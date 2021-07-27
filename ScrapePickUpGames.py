from bs4 import BeautifulSoup
from datetime import datetime
import requests
import json

events = {}
eventIndex = 0
for urlIndex in range(1, 103):
    URL = "https://dallasstars.maxgalaxy.net/Schedule.aspx?ID=" + str(urlIndex)
    page = requests.get(URL)
    soup = BeautifulSoup(page.text, 'html.parser')
    divs = soup.find_all("div", {'class': 'rsApt rsAptColor'})
    for div in divs:
        event = {}
        div.clear()
        div = div.get("title")
        div = BeautifulSoup(div, 'html.parser')
        labels = div.find_all("div", {'class': 'wrToolTipLabel clear'})
        labelIndex = 0
        for value in div.find_all("div", {'class': 'wrToolTipValue'}):
            label = labels[labelIndex].text.replace("': ", "").replace(":", "").replace(" ", "")
            event[label] = value.text
            labelIndex += 1
        events[eventIndex] = event
        eventIndex += 1

for eventIndex in events:
    eventType = events[eventIndex]["EventType"]
    eventDate = datetime.strptime(events[eventIndex]["Date"], "%m/%d/%Y").strftime("%m-%d-%y")
    jsonBody = {"date": eventDate}

    if eventType == "Adult Drop-In":
        jsonBody["type"] = "dropIn"
    elif eventType == "Public Session":
        jsonBody["type"] = "publicSession"
    elif eventType == "Adult Stick & Puck":
        jsonBody["type"] = "stickNPuck"
    elif eventType == "Freestyle Session":
        jsonBody["type"] = "freestyleSession"
    elif eventType == "Parent & Child Open Hock.":
        jsonBody["type"] = "parentChildOpenHockey"
    elif eventType == "Skating Pro-Time":
        jsonBody["type"] = "proSkatingTime"
    else:
        print("failure")
        continue

    response = requests.post('http://127.0.0.1:5000/hockeyEvent/create', data=json.dumps(jsonBody), headers={"content-type":"application/json"})
    print(response)