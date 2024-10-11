import subprocess
from time import sleep
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


chromeDriverPath = 'C:/Users/utsav/OneDrive/Desktop/Eventbrite-Scraping/chromeDriver/chromedriver.exe'

options = Options()
options.add_experimental_option("debuggerAddress", "localhost:8989")
options.add_argument(f"webdriver.chrome.driver={chromeDriverPath}")
options.add_argument("--disable-notifications")


def getDataFromFile():
    try:
        with open('eventData.json', 'r') as jsonFile:
            allEventData = json.load(jsonFile)
    except FileNotFoundError:
        allEventData = {}
    return allEventData

def putDataToFile(taazaMaal):
    with open('eventData.json', 'w') as jsonFile:
        json.dump(taazaMaal, jsonFile, indent=4)

def prepareChromeAndSelenium():
    chrome_process = subprocess.Popen([
        'C:/Program Files/Google/Chrome/Application/chrome.exe',
        '--remote-debugging-port=8989',
        '--user-data-dir=C:/Users/utsav/OneDrive/Desktop/Eventbrite-Scraping/chromeData/'
    ])
    driver = webdriver.Chrome(options=options)
    return chrome_process, driver

def runSelenium(thisDriver, mainLink):
    pageCounter = 1
    while True:
        thisDriver.get(f"{mainLink}{pageCounter}")
        try:
            eventData = getDataFromFile()
            eventList = WebDriverWait(thisDriver, 5).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "ul[class^='SearchResultPanelContentEventCardList-module__eventList']"))
            )
            
            eventItems = eventList.find_elements(By.TAG_NAME, "li")
            
            for eventItem in eventItems:
                try:
                    try:
                        eventItem.find_element(By.TAG_NAME, "aside")
                        continue
                    except:
                        thisData = eventItem.find_elements(By.CSS_SELECTOR, "section.event-card-details")[1]
                        thisDataa = thisData.find_element(By.CSS_SELECTOR, "a.event-card-link")
                        thisTitle = thisDataa.find_element(By.TAG_NAME, 'h3').text.strip()
                        thisID = thisDataa.get_attribute('data-event-id')
                        thisLink = thisDataa.get_attribute('href')
                        # print(thisTitle, thisID, thisLink)

                        if thisID not in eventData:
                            eventData[thisID] = {'eventURL': thisLink, 'title': thisTitle}
                except:
                    print("Exception occurred")
            putDataToFile(eventData)
        except:
            print("Pages Khatam Bhailu!")
            break
        pageCounter += 1

