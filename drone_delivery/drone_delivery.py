# -*- coding: utf-8 -*-
import os
import time
import cherrypy
from dronekit import connect, VehicleMode, LocationGlobalRelative

class DroneServer(object):
    def __init__(self):
        try:
            print("Connecting to vehicle...")
            self.vehicle = connect('/dev/ttyAMA0', wait_ready=True, baud=57600)
            print("Connected to vehicle")
        except Exception as e:
            print("Error connecting to vehicle:", e)
    
    def arm_and_takeoff(self, aTargetAltitude):
        """
        Arms vehicle and fly to aTargetAltitude.
        """

        print("Basic pre-arm checks")
        while not self.vehicle.is_armable:
            print(" Waiting for vehicle to initialise...")
            time.sleep(1)

        print("Arming motors")
        self.vehicle.mode = VehicleMode("GUIDED")
        self.vehicle.armed = True

        while not self.vehicle.armed:
            print(" Waiting for arming...")
            time.sleep(1)

        print("Taking off!")
        self.vehicle.simple_takeoff(aTargetAltitude)

        while True:
            print(" Altitude: ", self.vehicle.location.global_relative_frame.alt)
            if self.vehicle.location.global_relative_frame.alt >= aTargetAltitude * 0.95:
                print("Reached target altitude")
                break
            time.sleep(1)

    def return_to_launch(self):
        """
        Command the drone to return to the launch (home) position.
        """
        print("Returning to Launch")
        self.vehicle.mode = VehicleMode("RTL")

    def land(self):
        """
        Initiate landing sequence.
        """
        print("Landing")
        self.vehicle.mode = VehicleMode("LAND")
        while self.vehicle.armed:
            print(" Waiting for disarming...")
            time.sleep(1)
        print("Drone disarmed")

    @cherrypy.expose
    def index(self):
        return open(os.path.join(os.path.dirname(__file__), 'html/index.html'))

    @cherrypy.expose
    def tracker(self):
        return open(os.path.join(os.path.dirname(__file__), 'html/track.html'))

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def track(self, lat, lon):
        try:
            lat = float(lat)
            lon = float(lon)
            target_location = LocationGlobalRelative(lat, lon, 10)  # Altitude 10 meters

            print("Mission starting")
            self.arm_and_takeoff(10)  # Décoller à 10 mètres

            print("Going towards target location")
            self.vehicle.simple_goto(target_location)

            while True:
                print(" Current Altitude: ", self.vehicle.location.global_relative_frame.alt)
                if self.vehicle.location.global_relative_frame.alt >= target_location.alt * 0.95:
                    print("Reached target location")
                    break
                time.sleep(1)

            time.sleep(10)  # Maintenir la position pendant 10 secondes

            print("Returning to Launch")
            self.return_to_launch()

            return {"status": "Mission completed"}

        except Exception as e:
            print("Error during mission:", e)
            self.land()
            return {"status": "Error during mission", "error": str(e)}

if __name__ == '__main__':
    conf = {
        '/': {
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/html': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'html'
        }
    }
    cherrypy.config.update({'server.socket_host': '0.0.0.0', 'server.socket_port': 8080})
    cherrypy.quickstart(DroneServer(), '/', conf)

