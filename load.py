import json
import os
import pyodbc
import datetime
import decimal


server = ''
database = ''
username = ''
password = ""
driver= '{ODBC Driver 17 for SQL Server}'
sql_connection = pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = sql_connection.cursor()

query_file = "SELECT_HourlyAverage.sql"

# executes a select query and exports to json
with open(query_file) as f:
    query = f.read()
    cursor.execute(query)
    rows = cursor.fetchall()
    columns = [column[0] for column in cursor.description]
    cursor.commit()
    cursor.close()

def serialize(o):
    if isinstance(o, datetime.datetime):
        return str(o)

data = []
for row in rows:
    data.append(dict(zip(columns, row)))

with open('data.json', 'w') as f:
    json.dump(data, f, default = str)
    rows = json.loads(json.dumps(data, default = str))



# entry class
entryList= []

class Entry:
    def __init__(self, currentTime, forecastTime, currentTemp, forecast_list):
        self.currentTime = currentTime
        self.forecastTime = forecastTime
        self.currentTemp = currentTemp
        self.forecast_list = forecast_list


#build objects
for row in rows:
    currentTime = row["current_time"]
    forecastTime = row["forecast_api_time"]
    currentTemp = row["current_temp"]
    entryList.append(Entry(currentTime, forecastTime, currentTemp,[]))

#populate object.forecast_list with objects
c = 0
hours = 0

for i in entryList:
    if hours > 8: hours = 8
    if c != 0:
        for x in range (c-hours,c):
            i.forecast_list.append(entryList[x])
    hours += 1
    c += 1




# confirm objects
for x in entryList:
    print(x)
    print("Current time :" + str(x.currentTime))
    print("Forecast Time: " + str(x.forecastTime))
    print("Current Temp: " + str(x.currentTemp))
    print("Entries that guessed forecasted this period: " + str(len(x.forecast_list)))
    print("Forecasted from: ") 
    q = ""
    for i in x.forecast_list:
        q += i.currentTime + " " + str(i) + "\n"
    print(q)
    print(" ")
