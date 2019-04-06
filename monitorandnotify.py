'''
    Monitor And Notify
    LACHLAN NEWMAN
'''

from datetime import date
import json
from sense_hat import SenseHat
from pushnotification import PushNotification
from database import Database


class MonitorAndNotify:
    '''
    Object used to monitor the temperature
    and humidity using the sense hat system
    and log the data to a database every minute.
    This class will also send a push notifcation only once
    when the temperature or humidity is above or below the
    values in a config file.
    :param config: Config file with min and max humidity and temperature
    :type config: dict
    '''
    def __init__(self, config):
        self._sense_hat = SenseHat()
        self._max_temperature = config['max_temperature']
        self._min_temperature = config['min_temperature']
        self._max_humidity = config['max_humidity']
        self._min_humidity = config['min_humidity']


    def outside_temperature_range(self, temperature):
        '''
        Returns whether or not the temperature is above or below the min or max
        :param temperature:
        :return: Boolean
        '''
        return self._min_temperature < temperature < self._max_temperature

    def outside_humidity_range(self, humidity):
        '''
        Returns whether or not the temperature is above or below the min or max
        :param humidity:
        :return: Boolean
        '''
        return self._min_humidity < humidity < self._max_humidity

    @property
    def temperature(self):
        '''
        returns the temmperature
        :return: double
        '''
        return self._sense_hat.get_temperature()

    @property
    def humidity(self):
        '''
        Returns the humdity
        :return: double
        '''
        return self._sense_hat.get_humidity()

    def push_notification(self):
        '''
        Sends a push notification
        '''
        PushNotification.send_notification_via_pushbullet("From Pi", "Temperature Outsde range")


if __name__ == '__main__':
    with open('/home/pi/Sensors_Database/config.json') as config_file:
        CONFIG = json.load(config_file)
        config_file.close()
    MONITOR_AND_NOTIFY = MonitorAndNotify(CONFIG)
    TABLE_NAME = 'temperature_humidity'
    DB = Database('/home/pi/Sensors_Database/db.json')
    #check if the table exist and if not create it
    DB.create_table(TABLE_NAME)
    # get temperature from the sensehat
    TEMPERATURE = MONITOR_AND_NOTIFY.temperature
    #get humidity from sense hat
    HUMIDITY = MONITOR_AND_NOTIFY.humidity
    #check if its outside range
    print('checking range of temp and humidity')
    OUTSIDE_RANGE = MONITOR_AND_NOTIFY.outside_temperature_range(TEMPERATURE) and \
                    MONITOR_AND_NOTIFY.outside_humidity_range(HUMIDITY)
    #check if notification has been pushed today
    DATE = date.today().strftime("%Y-%m-%d")
    PUSH_SENT = False
    # QUERY = """SELECT * FROM temperature_humidity where date = '{}' AND notification_pushed = 'true'""".format(DATE)
    DATA = DB.get_data()
    TODAYS_DATA = DATA.loc[(DATA.notification_pushed == 'true') & (DATA.date == DATE)]
    print(TODAYS_DATA)
    if TODAYS_DATA.empty:
        #use push pullet to send the nootification
        MONITOR_AND_NOTIFY.push_notification()
        PUSH_SENT = True
    # insert new values into the database
    VALUES = (TEMPERATURE, HUMIDITY, OUTSIDE_RANGE, PUSH_SENT)
    DB.insert(TABLE_NAME, VALUES)
    #close database
    DB.close()
