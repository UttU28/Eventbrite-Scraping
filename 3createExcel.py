import json
import re
from tqdm import tqdm
import pandas as pd
from datetime import datetime

def readAndIterateJson(filePath):
    with open(filePath, 'r') as jsonFile:
        return json.load(jsonFile)

def processTheData(data):
    columns = ['Title', 'Event URL', 'Start Date', 'Venue Name', 'Description']
    rows = []
    
    for eventId, eventData in tqdm(data.items(), desc="Processing Events"):
        title = eventData['title']
        eventURL = eventData['eventURL']
        description = eventData['description']
        venue = eventData['venue_name']
        startDate = datetime.fromisoformat(eventData['start_date'].replace("Z", "+00:00")).strftime("%B %d, %Y at %I:%M %p")

        rows.append([title, eventURL, startDate, venue, description])

    df = pd.DataFrame(rows, columns=columns)
    return df

if __name__ == "__main__":
    data = readAndIterateJson('data/eventData.json')
    df = processTheData(data)

    excel_file = 'events.xlsx'
    
    with pd.ExcelWriter(excel_file, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Events')
        
        workbook = writer.book
        worksheet = writer.sheets['Events']
        
        hyperlink_format = workbook.add_format({'color': 'blue', 'underline': 1})
        
        for row in range(1, len(df) + 1):  # Start from 1 to skip the header
            worksheet.write_url(row, 1, df.iloc[row - 1, 1], hyperlink_format)  # Column 1 is 'Event URL'
        
        worksheet.set_column('A:A', max(df['Title'].str.len().max(), len('Title')) + 2)
        worksheet.set_column('C:C', max(df['Start Date'].str.len().max(), len('Start Date')) + 2)
        worksheet.set_column('D:D', max(df['Venue Name'].str.len().max(), len('Venue Name')) + 2)

    print(f"Data successfully exported to {excel_file} with clickable links.")
