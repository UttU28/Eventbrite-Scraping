import json
import re
from tqdm import tqdm
from eventBright import fetchEventData, appendToJsonFile

NEGATIVE_FILTERS = [ 'Workshop', 'Training', 'Digital Marketing' ]
POSITIVE_FILTERS = [ 'Digital Assets', 'Digital Security', 'Real World Assets', 'Digital Tokenization', 'Fintech', 'Real Estate Tokenization', 'Blockchain', 'Tokenization', 'Token Summit', 'Crypto Summit' ]

def readAndIterateJson(filePath):
    with open(filePath, 'r') as jsonFile:
        return json.load(jsonFile)

def cleanTheText(wholeDict):
    nonAsciiPattern = re.compile(r'[^\x00-\x7F]+')
    keysToFilter = ['title', 'description', 'summary', 'event_address', 'venue_name']
    
    for key in keysToFilter:
        cleanedText = nonAsciiPattern.sub('', wholeDict[key])  
        cleanedText = re.sub(r'[^\S\r\n]+', ' ', cleanedText)  
        cleanedText = re.sub(r'[\n\r]', ' ', cleanedText)  
        cleanedText = re.sub(r'\s+', ' ', cleanedText).strip()  
        wholeDict[key] = cleanedText 

    return wholeDict

def checkFilters(filterList, mainText):
    mainText = re.sub(r'\s+', ' ', mainText.lower()).strip()
    return any(filterItem.lower() in mainText for filterItem in filterList)

def checkNegatives(eventData):
    return not checkFilters(NEGATIVE_FILTERS, eventData['title'])

def checkPositives(eventData):
    combinedText = eventData['summary'] + ' ' + eventData['description']
    return checkFilters(POSITIVE_FILTERS, combinedText)

def processEvents(data):
    for eventId, eventData in tqdm(data.items(), desc="Processing Events"):
        thisEventId, thisEventData = fetchEventData(eventId)
        
        if thisEventData:
            thisEventData['title'] = eventData['title']
            thisEventData['eventURL'] = eventData['eventURL']
            cleanedEventData = cleanTheText(thisEventData)

            if checkNegatives(cleanedEventData) and checkPositives(cleanedEventData):
                appendToJsonFile(thisEventId, cleanedEventData)


if __name__ == "__main__":
    data = readAndIterateJson('baseData.json')
    processEvents(data)
