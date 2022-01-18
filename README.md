# Drain
Periodically drain or charge mobile device battery to avoid overcharging. 
Monitor and control with Acroname USB hubs and Flask REST API. Tested on macOS.


## Endpoints
Local address: `0.0.0.0:5004`


`GET /api/status/` - Get current status for all hubs and ports

`GET /api/status/<string:udid>` - Get particular device status

`POST /api/connect/` - Connect all devices

`POST /api/connect/<string:udid>` Connect individual device by UDID`

`POST /api/disconnect/<string:udid>` - Disconnect individual device by UDID`

`POST /api/cycle/` - Put devices in charging cycle mode (charge to 80%, drain to 30%)

`GET /api/search/<string:udid>` - Find and get on which hub and port the given device is connected (Cycle mode only)

## Add devices
List of test devices is defined in file `devices.yaml`

Example:
```
devices:
  - name: Pixel 3XL
    os: Android
    udid: xxx
    hub_serial: 70000000
    hub_port: 1
  - name: iPhone XS Max
    os: iOS
    udid: xxx
    hub_serial: 40000000
    hub_port: 2
```
## Resolve dependencies (python3)
```
pip install -r requirements.txt
```

## Run server
```
./start.sh
```

Or run full command:
```
export FLASK_APP=src/main.py; export FLASK_ENV=production; flask run --host=0.0.0.0 --port=5004
```

## Run tests
```
pytest tests/tests.py
```