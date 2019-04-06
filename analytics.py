'''
    Analytics and Graph Generator
    LACHLAN NEWMAN
'''
import matplotlib.pyplot as plot
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd
from database import Database

class Analytics:
    '''
    Object is used to generate a graph based on temperature
    and humidity data
    '''
    def __init__(self, temperature_label, humidity_label, temperature_interval,
                 humidity_interval, date_label, date_format):
        self._temperature_label = temperature_label
        self._humidity_label = humidity_label
        self._temperature_interval = temperature_interval
        self._humidity_interval = humidity_interval
        self._date_label = date_label
        self._date_format = date_format

    def set_date_interval(self, axis):
        '''Set the date interval and format for the graphs'''
        axis[0].set(xlabel='Date', ylabel='Temperature Celcius')
        axis[1].set(xlabel='Date', ylabel='Humidity %')
        for axis in axis:
            axis.xaxis.set_major_locator(mdates.DayLocator())
            axis.xaxis.set_major_formatter(mdates.DateFormatter(self._date_format))

    def matplotlib_plot(self, data):
        '''Plots the data to a graph using the matplotlib library'''
        _, ax1 = plot.subplots()
        ax2 = ax1.twinx()
        self.set_date_interval((ax1, ax2))
        plot.plot('Date', 'Temperature', data=data)
        plot.plot('Date', 'Humidity', data=data)
        plot.show()

    def seaborn_plot(self, data):
        '''Plots the data to a graph using the seaborn library'''
        sns.set()
        _, ax1 = plot.subplots()
        ax2 = ax1.twinx()
        self.set_date_interval((ax1, ax2))
        sns.lineplot(x='Date', y='Temperature', data=data, ax=ax1)
        sns.lineplot(x='Date', y='Humidity', data=data, ax=ax2)
        plot.show()


if __name__ == '__main__':
    # Create Database Object
    DB = Database('db.json')
    # Return Data from Database
    DATA = DB.get_data()
    # Group Data into mean humidity and temperatures fro each day
    MEAN_DATA = DATA.groupby('date')['temperature', 'humidity'].mean().reset_index()
    #Create Analytics Object
    ANALYTICS = Analytics('Temperature', 'Humidity', 1, 1, 'Date', '%d-%m-%Y')
    # Plot the seaborn graph
    ANALYTICS.seaborn_plot(MEAN_DATA)
    # plot the matlotlib graph
    ANALYTICS.matplotlib_plot(MEAN_DATA)
