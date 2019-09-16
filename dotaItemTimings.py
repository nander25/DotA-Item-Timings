# Written by: Noah Anderson
import requests
import json
import heroInfo

# Change number to easily readable percentage with 2 decimal points
def changeToPercent(n):
    perc = n * 100
    perc = round(perc, 2)
    return perc

# Converts a time in seconds to a Min:Sec format
def changeToTime(n):
    time = int(n)
    seconds = time % 60
    minutes = time // 60
    if seconds == 0:
        return str(minutes) + ':00'
    elif minutes == 0:
        return "00:" + str(seconds)
    else:
        return str(minutes) + ':' + str(seconds)

# Asks user to enter the name of a hero in DotA 2
found = False    
while found == False:
    inpt = str(input("Please enter the name of the Hero: "))
    
    # Find the id of user input
    heroID = heroInfo.getHeroID(inpt)
    if heroID != -1:
        found = True

# Sends request to the OpenDota API to get data on item timings
parameter = {"hero_id" : hero}
r = requests.get("https://api.opendota.com/api/scenarios/itemTimings", params = parameter)

itemTimings = r.json()

winrate = []

# Removes data where there are less than 100 games played for that item.
cleanedTimings = [s for s in itemTimings if int(s["wins"]) > 100]

# Creates a sorted list with the best winrate for each item
for items in cleanedTimings:
    wr = changeToPercent((float(items["wins"]) / float(items["games"])))
    
    if wr < winrate[index]["winrate"]:
            winrate[index] = {"item_name": items["item"], "item_time": changeToTime(items["time"]), "winrate": wr}
    else:          
        winrate.append({"item_name": items["item"], "item_time": changeToTime(items["time"]), "winrate": wr})

# Sort in order of highest winrate first
sortedWinrate = sorted(winrate, key = lambda i: i["winrate"], reverse=True)

# Print the list
for i in sortedWinrate:
    print("Item name: ", i["item_name"], "Timing: ", i["item_time"], " Winrate: ", i["winrate"], "%")
