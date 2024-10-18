import json
import pandas as pd
import re

NEGATIVE_FILTERS = ['Workshop', 'Training', 'Digital Marketing', 'Job Fair', 'Hackathon', 'Career Consultation', 'Biologics', 'Meditation', 'Book Club', 'Networking']
POSITIVE_FILTERS = ['Digital Assets', 'Digital Security', 'Real World Assets', 'Digital Tokenization', 'Fintech', 'Real Estate Tokenization', 'Blockchain', 'Tokenization', 'Token Summit', 'Crypto Summit', 'Venture Capital', 'Fintech']
# POSITIVE_FILTERS = [ "Geothermal", "Clean Energy", "Green energy", "Sustainable Practices", "Renewable Resources", "Eco-friendly", "Carbon Neutral", "Solar Power", "Wind Energy", "Hydropower", "Energy Efficiency", "Zero Emissions", "Circular Economy", "Organic Farming", "Biodiversity Conservation", "Electric Vehicles", "Waste Reduction", "Sustainable Agriculture" ]

locations = {
    "singapore": "Singapore",
    "united-arab-emirates": "Abu_Dhabi",
    "hong-kong-sar": "Hong_Kong",
    "united-kingdom--london": "London",
    "ny--new-york": "New_York",
    "united-states--texas": "Texas",
    "united-states--florida": "Florida",
    "united-states--california": "California",
    "south-korea--seoul": "Seoul",
    "germany--frankfurt-am-main": "Frankfurt",
    "switzerland--geneve": "Geneva"
}

def readAndIterateJson(filePath):
    with open(filePath, 'r') as jsonFile:
        return json.load(jsonFile)

def checkFilters(filterList, mainText):
    mainText = re.sub(r'\s+', ' ', mainText.lower()).strip()
    return any(filterItem.lower() in mainText for filterItem in filterList)

def checkNegatives(eventData):
    return not checkFilters(NEGATIVE_FILTERS, eventData['title'])

def checkPositives(eventData):
    combinedText = eventData['summary'] + ' ' + eventData['description']
    return checkFilters(POSITIVE_FILTERS, combinedText)

def main():
    data = readAndIterateJson('data/eventData.json')  
    tagged_data = {}

    for event_id, event_info in data.items():
        if event_info.get('hasData'):
            if checkNegatives(event_info) and checkPositives(event_info):
                tag = event_info['tag']
                if tag not in tagged_data:
                    tagged_data[tag] = []
                
                start_date = pd.to_datetime(event_info['start_date']).strftime('%b %d %Y')
                
                tagged_data[tag].append({
                    'Title': event_info['title'],
                    'Start Date': start_date,
                    'Event URL': event_info['eventURL'],
                    'Venue Name': event_info['venue_name'],
                    'Description': event_info['description'],
                    'OGStDate': event_info['start_date']
                })

    excel_file = 'eventBrightEvents.xlsx'
    # excel_file = 'All_Events.xlsx'
    
    with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
        for tag, events in tagged_data.items():
            df = pd.DataFrame(events)
            
            df.sort_values(by='OGStDate', inplace=True)
            df.drop(columns=['OGStDate'], inplace=True)
            
            df.to_excel(writer, index=False, sheet_name=f'{locations[tag]}-Events')
            
            workbook = writer.book
            worksheet = writer.sheets[f'{locations[tag]}-Events']
            
            hyperlink_format = workbook.add_format({'color': 'blue', 'underline': 1})
            
            for row in range(1, len(df) + 1):
                worksheet.write_url(row, 2, df.iloc[row - 1, 2], hyperlink_format)
            
            worksheet.set_column('A:A', 50)
            worksheet.set_column('B:B', 20)
            worksheet.set_column('C:C', 20)
            worksheet.set_column('D:D', 40)
            worksheet.set_column('E:E', max(df['Description'].str.len().max(), len('Description')) + 2)

    print(f"Data successfully exported to {excel_file} with clickable links.")

if __name__ == "__main__":
    main()
