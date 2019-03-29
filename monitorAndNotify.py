
from datetime import datetime
from sense_hat import SenseHat
import psycopg2
import json


def outsite_range(min,max,value):
    return (min <= value <= max)

with open('config.json') as config_file:
    config = json.load(config_file)


time = datetime.now().strftime("%H:%M")
sense = SenseHat()
temp = sense.get_temperature()
print(outsite_range(config['min_temperature'],config['max_temperature'],temp))
humidity = sense.get_humidity()
print(temp)
try:
    connection = psycopg2.connect(user = "pi",
                                  password = "[password]",
                                  host = "localhost",
                                  port = "5432",
                                  database = "pi")
    cursor = connection.cursor()
    create_table_query = """ CREATE TABLE IF NOT EXISTS temp_humidity(
                            temperature FLOAT not null,
                            humidity FLOAT not null,
                            timestamp TIMESTAMP not null
                            )"""
    cursor.execute(create_table_query)
    postgres_insert_query = """ INSERT INTO temp_humidity (temperature,humidity,timestamp) VALUES (%s,%s,now())"""
    record_to_insert = (temp,humidity)
    cursor.execute(postgres_insert_query, record_to_insert)
    connection.commit()
    print("Table created successfully in PostgreSQL ")



except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
finally:
    #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            print("PostgreSQL connection is closed")