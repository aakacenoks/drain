# Drain
Periodically drain or charge mobile device battery to avoid overcharging. 
Monitor and control with Acroname USB hubs and Flask REST API. Tested on macOS.


## Endpoints
Local address: `0.0.0.0:5004`


`GET /api/status/` - Get current device status

`POST /api/connect/` - Connect all devices

`POST /api/cycle/` - Put devices in charging cycle mode (charge to 80%, drain to 30%)

## Add devices
List of test devices is defined in file `config/devices.yaml`

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
pytest test/tests.py
```