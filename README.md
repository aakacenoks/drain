# Drain
Periodically drain or charge mobile device battery to avoid overcharging. 
Monitor and control with Acroname USB hubs and Flask REST API.


## Add devices
List of test devices is defined in file `config/devices.yaml`

Example:
```
devices:
  - name: Pixel 3XL
    os: Android
    udid: 98261FFFF001GR
    hub_serial: 74937564
    hub_port: 1
  - name: iPhone XS Max
    os: iOS
    udid: 1faff2315aa7d5ce8880d5e0df3f589e714141e6
    hub_serial: 44933564
    hub_port: 2
```
## Resolve dependencies
```
pip install -r requirements.txt
```

## Run server
```
export FLASK_APP=src/main.py; export FLASK_ENV=production; flask run
```

## Run tests
```
pytest test/tests.py
```