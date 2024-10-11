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
        print(f'Error fetching event data: {response.status_code}')
        return None

def fetch_event_data(event_id):
    url1 = f'https://www.eventbrite.com/api/v3/events/{event_id}/?expand=venue'
    data1 = makeAPIRequest(url1)
    url2 = f'https://www.eventbrite.com/api/v3/events/{event_id}/structured_content/?purpose=listing'
    data2 = makeAPIRequest(url2)

    if data1 and data2:
        htmlContent = data2['modules'][0]['data']['body']['text']
        soup = BeautifulSoup(htmlContent, 'html.parser')
        thisSummary = soup.get_text(separator=' ', strip=True)
        thisEventURLs = [a['href'] for a in soup.find_all('a', href=True)]
        thisDescription = data1['description']['text']
        thisStartDate = data1['start']['utc']
        thisEndDate = data1['end']['utc']
        thisOnlineEvent = data1['online_event']
        thisIsTicketed = data1['is_externally_ticketed']
        thisEventLogo = data1['logo']['url']
        thisEventAddress = data1['venue']['address']['localized_address_display']
        thisVenueName = data1['venue']['name']

        event_data = {
            'summary': thisSummary,
            'event_urls': thisEventURLs,
            'description': thisDescription,
            'start_date': thisStartDate,
            'end_date': thisEndDate,
            'online_event': thisOnlineEvent,
            'is_ticketed': thisIsTicketed,
            'event_logo': thisEventLogo,
            'event_address': thisEventAddress,
            'venue_name': thisVenueName
        }

        # Append to existing JSON file
        append_to_json_file(event_id, event_data)

def append_to_json_file(event_id, event_data, filename='event_data.json'):
    try:
        # Read existing data
        with open(filename, 'r') as f:
            existing_data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        existing_data = {}

    # Add new event data
    existing_data[event_id] = event_data

    # Write updated data back to the file
    with open(filename, 'w') as f:
        json.dump(existing_data, f, indent=4)

if __name__ == "__main__":
    event_id = '965046077797'
    fetch_event_data(event_id)
