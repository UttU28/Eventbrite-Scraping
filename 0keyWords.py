import json
# "Dubai" : "united-arab-emirates--dby",

locations = {
    "Abu_Dhabi" : "united-arab-emirates",
    # "Singapore" : "singapore",
    # "Hong_Kong" : "hong-kong-sar",
    # "London" : "united-kingdom--london",
    # "New_York" : "ny--new-york",
    # "Texas" : "united-states--texas",
    # "Florida" : "united-states--florida",
    # "California" : "united-states--california",
    # "Seoul" : "south-korea--seoul",
    # "Frankfurt" : "germany--frankfurt-am-main",
    # "Geneva" : "switzerland--geneve"
}

formats = ["networking", "conventions", "conferences", "galas"]

keyWords = ["Digital Assets", "Digital Security", "Real World Assets", "Digital Tokenization", "Fintech", "Real Estate Tokenization", "Blockchain", "Tokenization", "Token Summit", "Crypto Summit"]

baseURL = "https://www.eventbrite.com/d/tx--texas-city/convention/digital-assets/"

def getAllLinks():
    allLinks = {}
    for _, thisLocation in locations.items():
        for thisFormat in formats:
            for keyWord in keyWords:
                thisKeyword = keyWord.lower().replace(' ','-')
                eventURL = f"https://www.eventbrite.com/d/{thisLocation}/{thisFormat}/{thisKeyword}/?page="
                allLinks[eventURL] = None
        break
    print(f"Total number of events: {len(allLinks)}")
    return allLinks

allLinks = getAllLinks()

# Save to a JSON file
with open('data/baseLinks.json', 'w') as json_file:
    json.dump(allLinks, json_file, indent=4)

print("Links saved to data/baseLinks.json")
