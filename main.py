from flask import Flask
import subprocess
import yaml

app = Flask(__name__)


def shell(command):
    byte_output = subprocess.check_output(command, shell=True)
    return byte_output.decode('UTF-8').rstrip()


def read_devices():
    with open("devices.yaml", 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            print(exc)


@app.route('/')
def hello_world():
    devices = read_devices()
    return devices['devices'][1]


if __name__ == '__main__':
    app.run()
