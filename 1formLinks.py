import json
from datetime import datetime, timezone
from time import sleep
from utils.primaryScraping import runSelenium, prepareChromeAndSelenium

def getCurrentTime(): return int(round(datetime.now(timezone.utc).timestamp()))

def readDataFromJson():
    with open('data/baseLinks.json', 'r') as json_file:
        baseLinks = json.load(json_file)
    return baseLinks

def saveDataToJSON(baseLinks):
    with open('data/baseLinks.json', 'w') as json_file:
        json.dump(baseLinks, json_file, indent=4)

def checkIfToday(currentTime):
    isToday = datetime.fromtimestamp(currentTime, tz=timezone.utc).date() == datetime.today().date()
    return isToday


baseLinks = readDataFromJson()
chromeProcess, thisDriver = prepareChromeAndSelenium()
try:
    for key, value in baseLinks.items():
        if not (value and checkIfToday(value)):
            baseLinks[key] = getCurrentTime()
            saveDataToJSON(baseLinks)
            runSelenium(thisDriver, key)
            sleep(1)
except:
    print("Hwllo")
finally:
    thisDriver.quit()
    chromeProcess.terminate()
