import json

with open('data.json') as i:
    data = json.load(i)

entryList= []

class Entry:
    def __init__(self, dateTime, currentTemp, forecast_list):
        self.dateTime = dateTime
        self.currentTemp = currentTemp
        self.forecast_list = forecast_list

for row in data:
    dateTime = row["forecast_api_time"]
    currentTemp = row["currentTemp"]
    entryList.append(Entry(dateTime, currentTemp,[]))

c = 0

for i in entryList:
    if c == 0:
        c += 1
        pass
    else:
        for x in range (0,c-1):
            i.forecast_list.append(entryList[x])
    c += 1

for x in entryList:
    print(x)
    print("API Time: " + str(x.dateTime))
    print("Current Temp: " + str(x.currentTemp))
    print("Entries that guessed forecasted this period: " + str(len(x.forecast_list)))
    print("Forecasted from: ") 
    q = ""
    for i in x.forecast_list:
        q += i.dateTime + "\n"
    print(q)
    print(" ")
