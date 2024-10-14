import json
import os
# "Dubai" : "united-arab-emirates--dby",

locations = {
    "Singapore" : "singapore",
    "Abu_Dhabi" : "united-arab-emirates",
    "Hong_Kong" : "hong-kong-sar",
    "London" : "united-kingdom--london",
    "New_York" : "ny--new-york",
    "Texas" : "united-states--texas",
    "Florida" : "united-states--florida",
    "California" : "united-states--california",
    "Seoul" : "south-korea--seoul",
    "Frankfurt" : "germany--frankfurt-am-main",
    "Geneva" : "switzerland--geneve"
}

formats = ["networking", "conventions", "conferences", "galas"]

keyWords = ["Digital Assets", "Digital Security", "Real World Assets", "Digital Tokenization", "Fintech", "Real Estate Tokenization", "Blockchain", "Tokenization", "Token Summit", "Crypto Summit"]

baseURL = "https://www.eventbrite.com/d/tx--texas-city/convention/digital-assets/"

def loadExistingLinks(filePath):
    if os.path.exists(filePath):
        with open(filePath, 'r') as json_file:
            return json.load(json_file)
    return {}

def getAllLinks():
    all_links = loadExistingLinks('data/baseLinks.json')
    for _, this_location in locations.items():
        for this_format in formats:
            for key_word in keyWords:
                this_keyword = key_word.lower().replace(' ', '-')
                event_url = f"https://www.eventbrite.com/d/{this_location}/{this_format}/{this_keyword}/?page="
                if event_url not in all_links:
                    all_links[event_url] = None
    print(f"Total number of events: {len(all_links)}")
    return all_links

all_links = getAllLinks()

with open('data/baseLinks.json', 'w') as json_file:
    json.dump(all_links, json_file, indent=4)

print("Links saved to data/baseLinks.json")