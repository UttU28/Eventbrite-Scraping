import json
import re
import sys
from tqdm import tqdm
from utils.eventBright import fetchEventData, appendToJsonFile

NEGATIVE_FILTERS = ['Workshop', 'Training', 'Digital Marketing', 'Job Fair', 'Hackathon']
POSITIVE_FILTERS = ['Digital Assets', 'Digital Security', 'Real World Assets', 
                    'Digital Tokenization', 'Fintech', 'Real Estate Tokenization', 
                    'Blockchain', 'Tokenization', 'Token Summit', 'Crypto Summit']

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
    for eventID, eventData in tqdm(baseData.items(), desc="Processing Events"):
        if eventID in existingData.keys(): continue
        
        thisEventID, thisEventData = fetchEventData(eventID, API_KEY)
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


if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            currentTokenIndex = int(sys.argv[1])
            if currentTokenIndex < 0 or currentTokenIndex >= len(accessTokens):
                raise ValueError("Token index out of range.")
            else:
                baseData = readAndIterateJson('data/baseData.json')
                existingData = readAndIterateJson('data/eventData.json')
                processEvents(baseData, existingData, accessTokens[currentTokenIndex])
        except ValueError as e:
            print(f"Invalid token index: {e}")
            sys.exit(1)
