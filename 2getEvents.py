import json
import re
import sys
from tqdm import tqdm
from utils.eventBright import fetchEventData, appendToJsonFile
from time import sleep

NEGATIVE_FILTERS = ['Workshop', 'Training', 'Digital Marketing', 'Job Fair', 'Hackathon', 'Career Consultation', 'Biologics', 'Meditation', 'Book Club', 'Networking']
POSITIVE_FILTERS = ['Digital Assets', 'Digital Security', 'Real World Assets', 'Digital Tokenization', 'Fintech', 'Real Estate Tokenization', 'Blockchain', 'Tokenization', 'Token Summit', 'Crypto Summit']

accessTokens = ['N7TRZJ6UEDZ7AXI36BZR', 'HTEBOZLFTTQHGGRHGH', 'T2N7FX43RKVI3OFQRE', 'VLEMREODHYNVPL6VHIO3']

def readAndIterateJson(filePath):
    try:
        with open(filePath, 'r') as jsonFile:
            return json.load(jsonFile)
    except:
        return {}

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

def processEvents(baseData, existingData, API_KEY):
    try:
        for eventID, eventData in tqdm(baseData.items(), desc="Processing Events", ascii=' >-'):
            if eventID in existingData.keys(): continue
            
            thisEventID, thisEventData = fetchEventData(eventID, API_KEY)
            if thisEventData.get('hasData') == 'SLEEP':
                break

            if thisEventData.get('hasData'):
                thisEventData['tag'] = eventData['tag']
                thisEventData['title'] = eventData['title']
                thisEventData['eventURL'] = eventData['eventURL']
                cleanedEventData = cleanTheText(thisEventData)

                appendToJsonFile(thisEventID, cleanedEventData)
                # if checkNegatives(cleanedEventData) and checkPositives(cleanedEventData):
                #     appendToJsonFile(thisEventID, cleanedEventData)
                # else: appendToJsonFile(thisEventID, {'hasData': False}) 
            else:
                appendToJsonFile(thisEventID, thisEventData)
    except:
        pass

def countdown(seconds):
    for i in range(seconds, 0, -1):
        sys.stdout.write(f"\r{i}... ")
        sys.stdout.flush()
        sleep(1)
    sys.stdout.write("\rTime's up!    \n")

if __name__ == "__main__":
    currentTokenIndex = 1
    while True:
        baseData = readAndIterateJson('data/baseData.json')
        existingData = readAndIterateJson('data/eventData.json')
        processEvents(baseData, existingData, accessTokens[currentTokenIndex])
        currentTokenIndex = (currentTokenIndex + 1) % 4
        print(f'SWITCHING THE API KEY to {currentTokenIndex}, going in SLEEP')
        countdown(10*60)