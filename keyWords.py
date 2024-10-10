
locations = {
    "Dubai" : "united-arab-emirates--dby",
    "Abu_Dhabi" : "united-arab-emirates",
    "Singapore" : "singapore",
    "Hong_Kong" : "hong-kong-sar",
    "London" : "united-kingdom--london",
    "New_York" : "ny--new-york",
    "Texas" : "united-states--texas",
    "Florida" : "united-states--florida",
    "California" : "united-states--california",
    "Seoul" : "south-korea--seoul",
    "Frankfurt" : "germany--frankfurt-am-main",
    "Geneva" : "switzerland--genève"
}

formats = ["networking", "conventions", "conferences", "galas"]

keyWords = ["Digital Assets", "Digital Security", "Real World Assets", "Digital Tokenization", "Fintech", "Real Estate Tokenization", "Blockchain", "Tokenization", "Token Summit", "Crypto Summit"]

baseURL = "https://www.eventbrite.com/d/tx--texas-city/convention/digital-assets/"

counter = 0
for keyWord in keyWords:
    for _, thisLocation in locations.items():
        for thisFormat in formats:
            counter += 1
            thisKeyword = keyWord.lower().replace(' ','-')
            eventURL = f"https://www.eventbrite.com/d/{thisLocation}/{thisFormat}/{thisKeyword}/?page="
            print(eventURL)
print(f"Total number of events: {counter}")