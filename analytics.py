from database import Database
import matplotlib.pyplot as plot
import matplotlib.dates as mdates
import pandas as pd
import seaborn as sns

class Analytics:

    def __init__(self,temperature_label,humidity_label,temperature_interval,
                humidity_interval,date_label,date_format):
        self._temperature_label = temperature_label
        self._humidity_label = humidity_label
        self._temperature_interval = temperature_interval
        self._humidity_interval = humidity_interval
        self._date_label = date_label
        # self._date_interval = date_interval
        self._date_format = date_format

    def data_from_db(self,db_config:str,table:str,columns:list):
        db = Database('db.json')
        query = "SELECT "
        for column in columns:
            query = query + "{},".format(column)
        query = query[:-1] + " from {}".format(table)
        results = db.query(query)
        return pd.DataFrame(results, columns=columns)

    def group_data_mean(self,df,group_by:list,aggregate_date:list):
        grouped_data = df.groupby('Date')
        return grouped_data['Temperature', 'Humidity'].mean().reset_index()

    def set_date_interval(self,axis):
        # Set temperature Axis Label
        axis[0].set(xlabel='Date', ylabel='Temperature Celcius')
        axis[1].set(xlabel='Date', ylabel='Humidity %')
        for ax in axis:
            ax.xaxis.set_major_locator(mdates.DayLocator())
            ax.xaxis.set_major_formatter(mdates.DateFormatter(self._date_format))

    def matplotlib_plot(self,data):
        _, ax1 = plot.subplots()
        ax2 = ax1.twinx()
        self.set_date_interval((ax1,ax2))
        plot.plot('Date', 'Temperature', data=data)
        plot.plot('Date', 'Humidity', data=data)
        plot.show()

    def seaborn_plot(self,data):
        sns.set()
        _, ax1 = plot.subplots()
        ax2 = ax1.twinx()
        self.set_date_interval((ax1,ax2))
        sns.lineplot(x='Date', y='Temperature', data=data,ax=ax1)
        sns.lineplot(x='Date', y='Humidity', data=data,ax=ax2)
        plot.show()



analytics = Analytics('Temperature','Humidity',1,1,'Date','%d-%m-%Y')
data = analytics.data_from_db('db.json','temperature_humidity',['Temperature','Humidity','Date'])
mean_data = analytics.group_data_mean(data,['Date'],['Temperature','Humidity'])
analytics.seaborn_plot(mean_data)
analytics.matplotlib_plot(mean_data)







# #
# dates = [result[2] for result in results]
# humidities = [result[1] for result in results]
# temps = [result[0] for result in results]

# data = pd.DataFrame({'temperatures':temps,'dates':dates,},index=index)
# mean_temps = data.groupBy(level=0).mean())

#
# mean_temps = np.mean(temps)
# std_temps = np.std(temps)
# cut_off = std_temps * 3
# lower,upper = mean_temps - cut_off, mean_temps + cut_off
# temps_outliers_removed = [result[0] for result in results if result[0] > lower and result[0] < upper]
# dates_outliers_removed = [result[2] for result in results if result[0] > lower and result[0] < upper]
#
# plot.plot(dates_outliers_removed,temps_outliers_removed)
# plot.gcf().autofmt_xdate()
# plot.ylim(np.min(temps),np.max(temps))
# plot.show()