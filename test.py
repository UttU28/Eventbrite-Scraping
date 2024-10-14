import json
from eventBright import fetchEventData, appendToJsonFile
import re
from tqdm import tqdm

def readAndIterateJson(file_path):
    with open(file_path, 'r') as json_file:
        return json.load(json_file)

data = readAndIterateJson('baseData.json')

negativeFilters = ['Workshop', 'Training', 'Digital Marketing']
positiveFilters = ['Digital Assets', 'Digital Security', 'Real World Assets', 'Digital Tokenization', 'Fintech', 'Real Estate Tokenization', 'Blockchain', 'Tokenization', 'Token Summit', 'Crypto Summit']

def checkTheseFiltersOn(filterList, mainText):
    mainText = re.sub(r'\s+', ' ', mainText.lower()).strip()
    for filter_item in filterList:
        if filter_item.lower() in mainText:
            return True
    return False

def checkNegatives(thisEventData):
    return not checkTheseFiltersOn(negativeFilters, thisEventData['title'])

def checkPositives(thisEventData):
    return checkTheseFiltersOn(positiveFilters, thisEventData['summary'] + ' ' + thisEventData['description'])

for key, value in tqdm(data.items(), desc="Processing Events"):
    thisEventID, thisEventData = fetchEventData(key)
    if thisEventData:
        thisEventData['title'] = value['title']
        thisEventData['eventURL'] = value['eventURL']

        if checkNegatives(thisEventData) and checkPositives(thisEventData):
            appendToJsonFile(thisEventID, thisEventData)
