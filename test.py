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
        event_data = response.json()
        return event_data
    else:
        print(f'Error fetching event data: {response.status_code}')
        return None


def fetch_event_data(event_id):
    url1 = f'https://www.eventbrite.com/api/v3/events/{event_id}/?expand=venue'
    data1 = makeAPIRequest(url1)
    url2 = f'https://www.eventbrite.com/api/v3/events/{event_id}/structured_content/?purpose=listing'
    # data2 = makeAPIRequest(url2)


    # htmlContent = data2['modules'][0]['data']['body']['text']
    # soup = BeautifulSoup(htmlContent, 'html.parser')
    # thisSummary = soup.get_text(separator=' ', strip=True)
    # thisEventURLs = [a['href'] for a in soup.find_all('a', href=True)]
    # print("Plain Text:", thisSummary)
    # print("URLs:", thisEventURLs)

    # thisDescription = data1['description']['text']
    # thisStartDate = data1['start']['utc']
    # thisEndDate = data1['end']['utc']
    # thisOnlineEvent = data1['online_event']
    # thisVenueID = data1['venue_id']
    # thisIsTicketed = data1['is_externally_ticketed']
    # thisEventLogo = data1['logo']['url']
    thisEventAddres = data1['venue']['address']
    thisEventLogo = data1['logo']['url']

if __name__ == "__main__":
    event_id = '965046077797'

    event_details = fetch_event_data(event_id)
    if event_details:
        print(event_details)