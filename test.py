import requests

def fetch_event_data(event_id, access_token):
    url = f'https://www.eventbrite.com/api/v3/events/{event_id}/'
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

if __name__ == "__main__":
    event_id = '965046077797'
    access_token = 'VLEMREODHYNVPL6VHIO3'

    event_details = fetch_event_data(event_id, access_token)
    if event_details:
        print(event_details)