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

    def data_from_db(self, table: str, columns: list):
        '''
        Opens a database object and returns a Dataframe
        wth the query results
        '''
        database = Database('db.json')
        query = "SELECT "
        for column in columns:
            query = query + "{},".format(column)
        query = query[:-1] + " from {}".format(table)
        results = database.query(query)
        return pd.DataFrame(results, columns=columns)

    def group_data_mean(self, dataframe):
        '''Groups the Data into mean temperature and humidity for each day'''
        grouped_data = dataframe.groupby('Date')
        return grouped_data['Temperature', 'Humidity'].mean().reset_index()

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
    DB = Database('db.json')
    QUERY = "SELECT * from temperature_humidity"
    DATA = DB.query(QUERY)
    print(DATA)
    grouped_data = DATA.groupby('date')
    print(grouped_data['temperature', 'humidity'].mean().reset_index())
    ANALYTICS = Analytics('Temperature', 'Humidity', 1, 1, 'Date', '%d-%m-%Y')
    DATA = ANALYTICS.data_from_db('db.json', 'temperature_humidity', ['Temperature', 'Humidity', 'Date'])
    MEAN_DATA = ANALYTICS.group_data_mean(DATA, ['Date'], ['Temperature', 'Humidity'])
    ANALYTICS.seaborn_plot(MEAN_DATA)
    ANALYTICS.matplotlib_plot(MEAN_DATA)
