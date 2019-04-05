'''
    CSV Report Generator
    LACHLAN NEWMAN
'''

import csv
import json
import pandas as pd
import numpy as np
from database import Database


class CreateReport:
    '''
        This Object is used for generating a csv containing
        the average minimum and maximum values in a database
        and outputting whether or not they are above the maximum
        and minimun values in a config file
        :param config: config file the min and max values of temperature and humidity
        :type config: dict
    '''
    __MIN_TEMPERATURE = "{}C below minimum temperature, "
    __MAX_TEMPERATURE = "{} C above maximum temperature, "
    __MIN_HUMIDITY = "{}% below minimum humidity, "
    __MAX_HUMIDITY = "{}C below maximum humidity, "

    def __init__(self, config: dict):
        self._outside_range = False
        self._min_temperature = config['min_temperature']
        self._max_temperature = config['max_temperature']
        self._min_humidity = config['min_humidity']
        self._max_humidity = config['max_humidity']

    def __check_temperature_min(self, temperature_min):
        if temperature_min < self._min_temperature:
            self._outside_range = True
            return abs(temperature_min - self._min_temperature)
        return None

    def __check_temperature_max(self, temperature_max):
        if temperature_max > self._max_temperature:
            self._outside_range = True
            return abs(temperature_max - self._max_temperature)
        return None

    def __check_humidity_min(self, humidity_min):
        if humidity_min < self._min_humidity:
            self._outside_range = True
            return abs(humidity_min - self._min_humidity)
        return None

    def __check_humidity_max(self, humidity_max):
        if humidity_max < self._min_humidity:
            self._outside_range = True
            return abs(humidity_max - self._min_humidity)
        return None

    def get_row(self, min_max_values: tuple):
        '''
        Checks to see whether or not the value for the
        maximum and minimum temperature and humidity
        is respectively above or below the values in the config fil
        passed
        :param min_max_values:
        :type min_max_values: tuple
        :return:
        '''
        temp_min_diff = self.__check_temperature_min(min_max_values.TempMin)
        temp_max_diff = self.__check_temperature_max(min_max_values.TempMax)
        humidity_min_diff = self.__check_humidity_min(min_max_values.HumidityMin)
        humidity_max_diff = self.__check_humidity_max(min_max_values.HumidityMax)

        row_string = '{} '.format("Bad" if self._outside_range else "Good")

        row_string += self.__MIN_TEMPERATURE.format(temp_min_diff) if temp_min_diff else ""
        row_string += self.__MAX_TEMPERATURE.format(temp_max_diff) if temp_max_diff else ""
        row_string += self.__MIN_HUMIDITY.format(humidity_min_diff) if humidity_min_diff else ""
        row_string += self.__MAX_HUMIDITY.format(humidity_max_diff) if humidity_max_diff else ""

        return [row.Date, row_string]


if __name__ == '__main__':

    # Name of table in the database
    TABLE_NAME = 'temperature_humidity'
    # Get access to the Database
    DB = Database('/home/pi/Sensors_Database/db.json')
    # Create the database query
    QUERY = """SELECT date,temperature,humidity from {}""".format(TABLE_NAME)
    # Create a Dataframe from the query
    DATA = pd.DataFrame(DB.query(QUERY), columns=['Date', 'Temperature', 'Humidity', ])
    # Group data  by date and get minimum and maximum values for temperature
    # and humidity
    GROUPED_DATA = DATA.groupby('Date')['Temperature', 'Humidity'].agg(
        {'Temperature': [np.max, np.min], 'Humidity': [np.max, np.min]}
    ).reset_index()
    # Reset the names of the grouped data columns
    GROUPED_DATA.columns = ['Date', 'TempMax', 'TempMin', 'HumidityMax', 'HumidityMin']

    # Open config file are get minimum and maximum temperature and humidity
    with open('/home/pi/Sensors_Database/config.json') as config_file:
        CONFIG = json.load(config_file)
    config_file.close()

    CREATE_REPORT = CreateReport(CONFIG)

    # Open file to produce report
    with open('report.csv', 'w') as reportFile:
        WRITER = csv.writer(reportFile)
        for row in GROUPED_DATA.itertuples():
            WRITER.writerow(CREATE_REPORT.get_row(row))
        reportFile.close()

    config_file.close()
