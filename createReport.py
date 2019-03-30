import csv
import json

from database import Database


def calc_difference(a, b):
    return abs(a - b)


table_name = 'temperature_humidity'
db = Database('/home/pi/Sensors_Database/db.json')
query = """SELECT date, MIN(temperature),MAX(temperature),MIN(humidity),MAX(humidity) from {} GROUP BY date""".format(
    table_name)
db_rows = db.query(query)

with open('/home/pi/Sensors_Database/config.json') as config_file:
    config = json.load(config_file)

with open('report.csv', 'w') as reportFile:
    writer = csv.writer(reportFile)
    for db_row in db_rows:
        min_temperature_string = ""
        max_temperature_string = ""
        min_humidity_string = ""
        max_humidity_string = ""
        outside_range = False

        if (db_row[1] < config['min_temperature']):
            difference = calc_difference(db_row[1], config['min_temperature'])
            min_temperature_string =  "{}C below minimum temperature, ".format(difference);
            outside_range = True
        if (db_row[2] > config['max_temperature']):
            difference = calc_difference(db_row[2], config['max_temperature'])
            max_temperature_string = "{}C above maximum temperature,".format(difference);
            outside_range = True
        if (db_row[3] < config['min_humidity']):
            difference = calc_difference(db_row[3], config['min_humidity'])
            min_humidity_string = "{}% below minimum humidity,".format(difference);
            outside_range = True
        if (db_row[4] > config['max_humidity']):
            difference = calc_difference(db_row[4], config['max_humidity'])
            max_humidity_string + "{}% above maximum humidity,".format(difference);
            outside_range = True
        outcome = "OK"
        if outside_range:
            outcome = "BAD: {}{}{}{}".format(min_temperature_string,max_temperature_string,min_humidity_string,max_humidity_string)
        row = [db_row[0].strftime('%Y-%m-%d'),outcome[:-1]]
        writer.writerow(row)
