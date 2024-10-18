import json
from bs4 import BeautifulSoup
from datetime import datetime
import os

outputFile = 'lumaData.json'
if os.path.exists(outputFile):
    with open(outputFile, 'r', encoding='utf-8') as jsonFile:
        sectionData = json.load(jsonFile)
else:
    sectionData = {}

with open('lumaData.html', 'r', encoding='utf-8') as file:
    htmlContent = file.read()

soup = BeautifulSoup(htmlContent, 'lxml')

timelineSections = soup.find_all(class_='timeline-section')

for section in timelineSections:
    dayAndDate = section.find(class_='timeline-title')
    if dayAndDate: 
        day = dayAndDate.find(class_='weekday').get_text(strip=True)
        date = dayAndDate.find(class_='date').get_text(strip=True) + ' 2024'
        
        cardWrappers = section.find_all(class_='card-wrapper')
        for cardWrapper in cardWrappers:
            try:
                linkTag = cardWrapper.find(class_='event-link')
                if linkTag and linkTag.name == 'a':
                    link = 'https://lu.ma' + linkTag.get('href')
                    timeAndTitle = cardWrapper.find(class_='info')
                    time = timeAndTitle.find(class_='event-time').get_text(strip=True)
                    title = timeAndTitle.find('h3').get_text(strip=True)
                    organizer = cardWrapper.find(class_='nowrap').get_text(strip=True).replace('By ', '')
                    try:
                        price = cardWrapper.find_all(class_='pill-label')[-1].get_text(strip=True)
                    except:
                        price = None
                    location = cardWrapper.find_all(class_='attribute')[-1].get_text(strip=True).replace('​','')

                    if linkTag.get('href')[1:] not in sectionData:
                        sectionData[linkTag.get('href')[1:]] = {
                            'day': day,
                            'link': link,
                            'date': date,
                            'time': time,
                            'title': title,
                            'organizer': organizer,
                            'price': price,
                            'location': location
                        }
            except Exception as e:
                print(f"Error parsing card data: {e}")

with open(outputFile, 'w', encoding='utf-8') as jsonFile:
    json.dump(sectionData, jsonFile, ensure_ascii=False, indent=4)

print("Data has been saved to output.json")
