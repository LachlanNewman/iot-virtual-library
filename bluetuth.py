from pushNotification import PushNotification
from sense_hat import SenseHat
import subprocess as sp

print("running bluetooth script")
sense_hat = SenseHat()
connected_devices = []

# Continuously check connected bluetooth devices
while True:
    # Get Current Temperature and Humidity
    temp = sense_hat.get_temperature()
    humidity = sense_hat.get_humidity()

    # List all currently connected bluetooth devices
    p = sp.Popen(["bt-device", "--list"], stdin=sp.PIPE, stdout=sp.PIPE, close_fds=True)
    (stdout, stdin) = (p.stdout, p.stdin)
    bt_devices = stdout.readlines()

    #check is any new bluetooth devices are connected
    for device in bt_devices[1:]:
        if(device not in connected_devices):
            PushNotification.send_notification_via_pushbullet('from Pi', 'Temp {}C Humidity {}%'.format(temp, humidity))
            connected_devices.append(device)

    #remove devices from connected_devices when device disconnects
    for device in connected_devices:
        if device not in bt_devices:
            connected_devices.remove(device)
