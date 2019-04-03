from pushNotification import PushNotification
from sense_hat import SenseHat
from database import Database
from datetime import date
import json

access_token = "o.wmY4EKIUDwm3f1KeVnS43h9cfFRTXBHl"

class MonitorAndNotify:

    def __init__(self, config_file):
        with open(config_file) as config_file:
            config = json.load(config_file)
        self._sense_hat = SenseHat()
        self._max_temperature = config['max_temperature']
        self._min_temperature = config['min_temperature']
        self._max_humidity = config['max_humidity']
        self._min_humidity = config['min_humidity']


    def outside_temperature_range(self, temperature):
        return self._min_temperature < temperature < self._max_temperature

    def outside_humidity_range(self, humidity):
        return self._min_humidity < humidity < self._max_humidity

    @property
    def temperature(self):
        return self._sense_hat.get_temperature()

    @property
    def humidity(self):
        return self._sense_hat.get_humidity()

    def push_notification(self):
        PushNotification.send_notification_via_pushbullet("From Pi","Temperature Outsde range")

table_name = 'temperature_humidity'
monitorAndNotify = MonitorAndNotify('/home/pi/Sensors_Database/config.json')
db = Database('/home/pi/Sensors_Database/db.json')
#check if the table exist and if not create it
db.create_table(table_name)
# get temperature from the sensehat
temperature = monitorAndNotify.temperature
#get humidity from sense hat
humidity = monitorAndNotify.humidity
#check if its outside range
print('checking range of temp and humidity')
outside_range = monitorAndNotify.outside_temperature_range(temperature) and \
                monitorAndNotify.outside_humidity_range(humidity)
#check if notification has been pushed today
date = date.today()
push_sent = False
select_query = """SELECT * FROM temperature_humidity 
                where date = '{}' AND notification_pushed = 'true'""".format(date)
results = db.query(select_query)
print(results)
if not db.query(select_query):
    #use push pullet to send the nootification
    print(results)
    monitorAndNotify.push_notification()
    push_sent = True  # type: bool

# insert new values into the database
values = (temperature, humidity, outside_range, push_sent)
db.insert(table_name, values)
#close database
db.close()