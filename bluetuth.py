from pushNotification import PushNotification
from sense_hat import SenseHat
import subprocess as sp

class Bluetuth:

    def __init__(self):
        self._connected_devices = []

    def bluetooth_devices(self):
        p = sp.Popen(["bt-device", "--list"], stdin=sp.PIPE, stdout=sp.PIPE, close_fds=True)
        (stdout, stdin) = (p.stdout, p.stdin)
        self._bt_devices = stdout.readlines()[1:]

    def check_new_devices(self):
        for device in self._bt_devices:
            if (device not in self._connected_devices):
                PushNotification.send_notification_via_pushbullet('from Pi',
                                                                  'to{} : Temp {}C Humidity {}%'.format(device, temp,
                                                                                                        humidity))
                self._connected_devices.append(device)

    def check_disconneted_devices(self):
        for device in self._connected_devices:
            if device not in self._bt_devices:
                self._connected_devices.remove(device)

print("running bluetooth script")
sense_hat = SenseHat()
bluetuth = Bluetuth()

# Continuously check connected bluetooth devices
while True:
    # Get Current Temperature and Humidity
    temp = sense_hat.get_temperature()
    humidity = sense_hat.get_humidity()

    # Get all currently connected bluetooth devices
    bluetuth.bluetooth_devices()

    # Check is any new bluetooth devices are connected
    bluetuth.check_new_devices()

    # Check if any devices have disconnected
    bluetuth.check_disconneted_devices()



