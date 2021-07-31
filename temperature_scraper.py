import pyodbc
import requests
import time
import logging
import ssl
import json

API_Key = ''




logging.basicConfig(filename='log.log', encoding='utf-8', level=logging.DEBUG, format='%(asctime)s %(levelname)-8s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logger = logging.getLogger("logger")
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(levelname)s;%(asctime)s;%(message)s",
                              "%Y-%m-%d %H:%M:%S")
ch.setFormatter(formatter)
logger.addHandler(ch)


with open('sql.json') as f:
    login = json.load(f)
server = login["server"]
database = login["database"]
username = login["username"]
password = login["password"]
driver= login["driver"]



# returns values in json/dict for sql insert
def getValues():
    weather_api_url = f"https://api.openweathermap.org/data/2.5/onecall?lat=43.658963&lon=-79.383846&appid={API_Key}"
    weather_data = requests.get(weather_api_url)
    weather_json = weather_data.json()
    returnEntry = {
        "entryTime" : time.strftime('%Y-%m-%d %H:%M:%S'),

        "current" : {
            "current_api_time" : time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(weather_json["current"]["dt"])),
            "currentTemp" : weather_json["current"]["temp"]
        },

        "forecast" : {
            "forecast_api_time" : time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(weather_json["hourly"][0]["dt"])),
            "temps" : {}

        }
    }
    c = 0
    for i in weather_json["hourly"]:
        hourly = i["temp"]
        returnEntry["forecast"]["temps"][c] = hourly
        c += 1
    return (returnEntry)


def insertEntry():

    entryList = getValues()
    entryTime = entryList["entryTime"]

    current_api_time = entryList["current"]["current_api_time"]
    currentTemp = entryList["current"]["currentTemp"]
    forecast_api_time = entryList["forecast"]["forecast_api_time"]
    temps = entryList["forecast"]["temps"]


    # build insert query
    query = "insert into Forecast (entryTime, current_api_time, currentTemp, forecast_api_time, "
    for i in range(0, 48):
        query += "forecast_temp_" + str(i) 
        if i < 47: query += ", "
    query += f") values ('{entryTime}', '{current_api_time}', {currentTemp}, '{forecast_api_time}', "

    for i in range(0, 48):
        query += str(temps[i])
        if i < 47: query += ", "
    query += ")"


    # query
    cursor.execute(query)
    cursor.commit()
    print(query)

#connect to sql server
pyodbc.pooling = False
sql_connection = pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = sql_connection.cursor()

def loop():
    try:
        while True:
            insertEntry()
            print("...")
            print("...")
            time.sleep(30)

    except pyodbc.Error as ex:
        sqlstate = ex.args[1]
        ch.debug(ex)
        ch.debug(sqlstate)
        print("sql error")
        sql_connection = pyodbc.connect('DRIVER='+driver+';SERVER=tcp:'+server+';PORT=1433;DATABASE='+database+';UID='+username+';PWD='+ password)
        cursor = sql_connection.cursor()
    
        loop()

    except ssl.SSLEOFError as ex:
        ch.debug(ex)
        print("ssl error")
        loop()
		
    except Exception as ex:
        ch.debug(ex)
        print("exception error")
        loop()

# main
loop()

