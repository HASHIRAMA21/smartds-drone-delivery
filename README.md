# SMARTDS Drone Delivery System

## Description

SMARTDS (Smart Drone Delivery System) is a comprehensive drone delivery application that combines flight simulation, mission management, real-time tracking, and an interactive web interface. The system uses DroneKit for drone communication, MongoDB for data persistence, Kafka for real-time messaging, and a modern web interface with Mapbox for geographical visualization.

## Project Architecture

The project is organized into two main modules:

### 1. SMARTDS Module (`/Drone/smartds/`)
Intelligent drone mission management system with database and messaging integration.

### 2. Drone Delivery Module (`/drone_delivery/`)
Web server for user interface and drone control via REST API.

## Key Features

### Drone Management
- Connection and control of drones via DroneKit
- Support for SITL simulator and physical drones
- Real-time monitoring of position, battery, and status
- Singleton system for unique drone instance management

### Mission System
- Creation and management of delivery missions
- Automatic tracking of ongoing missions
- Automatic calculation of nearest return station
- Support for surveillance missions with circular trajectories

### Web Interface
- Modern user interface with Mapbox integration
- Automatic geolocation
- Interactive destination selection on map
- Real-time drone tracking during missions
- Integrated address search functionality

### Integrations
- **MongoDB**: Storage for drones, missions, and stations
- **Apache Kafka**: Real-time telemetry data streaming
- **WebSockets**: Bidirectional communication for live tracking
- **Mapbox**: Mapping and geolocation services

## File Structure

```
vinc/
├── Drone/smartds/
│   ├── main.py                 # Main entry point
│   ├── Drone/drone.py          # Drone class for control and navigation
│   ├── Mission/mission.py      # Mission and MissionSurveillance classes
│   ├── requirements.txt        # Python dependencies
│   ├── .env                   # Environment variables
│   ├── script.sh              # Simulator launch script
│   └── test.py                # Test scripts
├── drone_delivery/
│   ├── drone_delivery.py      # CherryPy web server
│   ├── websocket_server.py    # WebSocket server for live data
│   └── html/
│       ├── index.html         # Main control interface
│       ├── track.html         # Real-time tracking page
│       └── assets/styles.css  # CSS styles
└── README.md
```

## Prerequisites

### Required Software
- Python 3.7+
- MongoDB (local or cloud)
- Apache Kafka
- DroneKit-SITL (for simulation)
- MAVProxy

### Python Dependencies
See `requirements.txt` for complete list. Main dependencies:
- dronekit
- pymongo
- kafka-python
- cherrypy
- websockets
- django (web framework)
- geopy (geographical calculations)

## Configuration

### Environment Variables (.env)
```bash
URL=mongodb://localhost:27017/
DATABASE_NAME=Drones
COLLECTION_DRONE=drones
COLLECTION_STATION=stations
COLLECTION_MISSION=missions
TOPIC=drone
KAFKA_BOOTSTRAP_SERVERS=localhost:9092
```

### MongoDB Database

#### "drones" Collection
```json
{
  "uid": "1234",
  "etat": "ON|OFF",
  "latitude": 0.0,
  "longitude": 0.0,
  "batterie": 100,
  "station": "station_name"
}
```

#### "missions" Collection
```json
{
  "drone": "drone_object_id",
  "etat": "EN COURS|TERMINEE",
  "type": "livraison|surveillance",
  "goal": "description",
  "position": {
    "lat": 0.0,
    "lng": 0.0
  }
}
```

#### "stations" Collection
```json
{
  "lieu": "station_name",
  "latitude": 0.0,
  "longitude": 0.0
}
```

## Installation and Deployment

### 1. Clone the Project
```bash
git clone https://github.com/HASHIRAMA21/smartds-drone-delivery.git
cd vinc
```

### 2. Install Dependencies
```bash
cd Drone/smartds
pip install -r requirements.txt
```

### 3. Database Configuration
- Install and start MongoDB
- Create "Drones" database
- Insert sample documents in collections

### 4. Kafka Configuration
- Install and start Apache Kafka
- Create "drone" topic

### 5. Launch Simulator
```bash
cd Drone/smartds
chmod +x script.sh
./script.sh
```

### 6. Launch SMARTDS Application
```bash
python main.py --connect udp:127.0.0.1:14551
```

### 7. Launch Web Server
```bash
cd drone_delivery
python drone_delivery.py
```

### 8. Access Interface
- Main interface: http://localhost:8080
- Tracking page: http://localhost:8080/tracker

## Usage

### Web Interface
1. Open web interface in browser
2. Use map to select destination
3. Click "Send" to start mission
4. Track drone in real-time on tracking page

### REST API
- `POST /track?lat={lat}&lon={lon}`: Start mission to specified coordinates

### Code Control
```python
from Drone.drone import Drone
from Mission.mission import Mission

# Create and connect drone
drone = Drone(url, database_name, collection_drone, topic, kafka_servers)
drone.connect_to_database()
drone.connectMyCopter()

# Create mission
mission = Mission(drone, "ON", "livraison", "livraison", url, database_name, collection_mission)
mission.connect_to_database()

# Execute mission
mission.my_mission()
```

## Mission Workflow

1. **Initialization**: Drone connects to database and simulator
2. **Mission Search**: Check for "EN COURS" missions assigned to drone
3. **Execution**:
   - Automatic takeoff
   - Navigation to destination
   - Landing at destination
   - Return to nearest station
4. **Finalization**: Update mission status and drone data

## Advanced Features

### Geolocation System
- Automatic calculation of nearest return station
- GPS coordinate support with metric precision
- Integration with Mapbox geocoding services

### Real-Time Telemetry
- Kafka streaming of position and battery data
- WebSockets for live interface updates
- Flight trajectory and performance history

### Security and Robustness
- Error handling for drone connections
- Mission parameter validation
- Singleton system to avoid instance conflicts

## Testing and Development

### Available Tests
- `test.py`: Basic connection and flight tests
- `t.py`: Kafka streaming tests

### Development Mode
For development, use SITL simulator which doesn't require physical hardware.

## Troubleshooting

### Common Issues

1. **Drone connection error**: Verify SITL simulator is running
2. **MongoDB error**: Verify MongoDB service is active
3. **Kafka error**: Check bootstrap servers configuration
4. **Geolocation issues**: Verify Mapbox API key

### Logs and Monitoring
- Flight logs displayed in console
- Kafka data can be monitored with dedicated tools
- Mission status persisted in database

## Technologies Used

- **DroneKit**: Python SDK for drone control
- **MongoDB**: NoSQL database
- **Apache Kafka**: Distributed streaming platform
- **CherryPy**: Python web framework
- **Mapbox GL JS**: Interactive mapping API
- **WebSockets**: Real-time communication
- **GeoPy**: Geographical calculations and distances

## Contributing

To contribute to the project:
1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Create a pull request

## License

This project is under MIT License. See LICENSE file for more details.

## Support

For any questions or issues, please open an issue on the GitHub repository or contact the SMARTDS development team.

## Contact

For technical inquiries and collaboration:
- Developer: HASHIRAMA21
- GitHub: [https://github.com/HASHIRAMA21](https://github.com/HASHIRAMA21)
- Specialization: Computer Vision and Machine Learning Engineering