import json
import requests
from bs4 import BeautifulSoup

def makeAPIRequest(url):
    access_token = 'VLEMREODHYNVPL6VHIO3'
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f'Error fetching data from {url}: {response.status_code}')
        return None

def fetchEventData(eventID):
    url1 = f'https://www.eventbrite.com/api/v3/events/{eventID}/?expand=venue'
    data1 = makeAPIRequest(url1)
    url2 = f'https://www.eventbrite.com/api/v3/events/{eventID}/structured_content/?purpose=listing'
    data2 = makeAPIRequest(url2)

    if data1 and data2 and not data1.get('online_event'):
        try:
            htmlContent = data2['modules'][0]['data']['body']['text']
            soup = BeautifulSoup(htmlContent, 'html.parser')
            thisSummary = soup.get_text(separator=' ', strip=True)
            thisEventURLs = [a['href'] for a in soup.find_all('a', href=True)]

            thisDescription = data1['description']['text'].strip()
            thisStartDate = data1['start']['utc']
            thisEndDate = data1['end']['utc']
            thisIsTicketed = data1['is_externally_ticketed']
            thisEventLogo = data1['logo']['url']
            thisEventAddress = data1['venue']['address']['localized_address_display']
            thisVenueName = data1['venue']['name']

            eventData = {
                'summary': thisSummary,
                'event_urls': thisEventURLs,
                'description': thisDescription,
                'start_date': thisStartDate,
                'end_date': thisEndDate,
                'is_ticketed': thisIsTicketed,
                'event_logo': thisEventLogo,
                'event_address': thisEventAddress,
                'venue_name': thisVenueName
            }

            return eventID, eventData
        except:
            return eventID, None
    return eventID, None

def appendToJsonFile(eventID, eventData, filename='eventData.json'):
    if eventData is None:
        return

    try:
        with open(filename, 'r') as f:
            existing_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = {}

    existing_data[eventID] = eventData

    with open(filename, 'w') as f:
        json.dump(existing_data, f, indent=4)

if __name__ == "__main__":
    eventIDs = ['965046077797', '1026778029727']  # Add more event IDs as needed
    for eventID in eventIDs:
        eventID, eventData = fetchEventData(eventID)
        appendToJsonFile(eventID, eventData)
