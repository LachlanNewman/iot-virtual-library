'''
    Bluetooth Notification Sender
    LACHLAN NEWMAN
'''

import subprocess as sp
from sense_hat import SenseHat
from pushnotification import PushNotification

class Bluetuth:
    '''
    This Object is used to check for the currently
    connected bluetooth devices and
    send a push notification to newly connected bluetooth devices
    '''
    def __init__(self):
        self._connected_devices = []
        self._bt_devices = None

    def bluetooth_devices(self):
        '''
        Checks what currently connected bluetooth devices are
        available
        '''
        terminal = sp.Popen(["bt-device", "--list"], stdin=sp.PIPE, stdout=sp.PIPE, close_fds=True)
        (stdout, _) = (terminal.stdout, terminal.stdin)
        self._bt_devices = stdout.readlines()[1:]

    def check_new_devices(self):
        '''
        checks to see what new devices are
        available to be connect by bluetooth
        '''
        for device in self._bt_devices:
            if device not in self._connected_devices:
                PushNotification.send_notification_via_pushbullet(
                    'from Pi', 'to {} : Temp {}C Humidity {}%'.format(device, TEMP, HUMIDITY)
                )
                self._connected_devices.append(device)

    def check_disconneted_devices(self):
        '''
        Checks to see if any previously connected
        devices have been disconnected
        '''
        for device in self._connected_devices:
            if device not in self._bt_devices:
                self._connected_devices.remove(device)

if __name__ == '__main__':
    print("running bluetooth script")
    SENSE_HAT = SenseHat()
    BLUETUTH = Bluetuth()
    # Continuously check connected bluetooth devices
    while True:
        # Get Current Temperature and Humidity
        TEMP = SENSE_HAT.get_temperature()
        HUMIDITY = SENSE_HAT.get_humidity()
        # Get all currently connected bluetooth devices
        BLUETUTH.bluetooth_devices()
        # Check is any new bluetooth devices are connected
        BLUETUTH.check_new_devices()
        # Check if any devices have disconnected
        BLUETUTH.check_disconneted_devices()
