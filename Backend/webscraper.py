from bs4 import BeautifulSoup
import requests
from selenium import webdriver
import csv
import unidecode

url = "https://fbref.com/en/comps/9/stats/Premier-League-Stats#all_stats_standard"



# Launch a headless Chrome browser
options = webdriver.ChromeOptions()
options.add_argument('--headless')
driver = webdriver.Chrome(options=options)

# Suppress browser console errors and warnings
options.add_argument('--log-level=3')#

driver = webdriver.Chrome(options=options)

driver.get(url)

# Get the page source after JavaScript has rendered the content
page_source = driver.page_source

# Close the browser
driver.quit()



#Derives country name from image source
def derive_country(country):
    #Empty list
    country_name = []
    #Retrieve image path
    path = country["href"]
    #Turn string format of path into lsit
    path = list(path)
    #Image path is built from slashes, use them to identify position of country
    slash_count = 0

    for j in range(0, len(path)):
        if path[j] == '/':
            slash_count+=1
        
        if slash_count == 4:
            index = j + 1
            break
    
    #Country name ends at dash
    while path[index] != '-':
        country_name.append(path[index])
        index+=1
    
    #Return value
    return (''.join(country_name))
    
#Derives position from 2 characters
def derive_position(position):
    if position == "DF":
        return "Defender"
    
    elif position == "DF,MF" or position == "MF,DF":
        return "Defensive Midfielder"
    
    elif position == "MF":
        return "Midfielder"
    
    elif position == "FW,MF" or position == "MF,FW":
        return "Attacking Midfielder"
    
    elif position == "FW":
        return "Forward"
    
    else:
        return "Goalkeeper"


def storefile(name, nationality, position, team, age, games, minutes, goals, assists, goal_assists, yellow_cards, red_cards):
    #Give data to append, including name, country, position, etc
    data_to_append = [name, nationality, position, team, age,
                     games, minutes, goals, assists, goal_assists, yellow_cards, red_cards]
    
    #Open CSV file
    file = open('PlayerStats.csv', 'a', newline='')
    #Instatiate CSV object
    writer = csv.writer(file)

    #Write data to append into file
    writer.writerow(data_to_append)

    #Close file
    file.close()








#Parses html code of entire website
soup = BeautifulSoup(page_source, "html.parser")

#Parses table containing player stats from parsed html code
results = soup.find('table', class_="min_width sortable stats_table shade_zero now_sortable sticky_table eq2 re2 le2")

#Extract tablerows
tablerows = results.find_all('tr')

#Pre Initialises all variables outside of the loop
player_name = ""
nationality = ""
position = ""
team = ""
age = ""
games = ""
minutes = ""
goals = ""
assists = ""
goal_assists = ""
yellow_cards = ""
red_cards = ""

#PlayerStats
#Writes all of the Names
for tablerow in tablerows:

    table_values = tablerow.find_all('td')
    
    for tabletext in table_values:
        #Ensures only statistics within the table are scraped
        type = tabletext["data-stat"] 

        #Scrapes all of the Names
        if type == "player":
            name = tabletext.find('a') #Loacates and scrapes hyperlink associated with name
            name = name.text.strip() #Cleans element until you are just left with the name written
            player_name = str(name) #Converts to string
            player_name = unidecode.unidecode(player_name) #Eliminate accents
    
        #Scraoes all of the nationalities    
        elif type == "nationality":
            country = tabletext.find('a') #Locates nationality image hyperlink
            nationality = derive_country(country) #Extracts country name from nationality
            nationality = unidecode.unidecode(nationality)
    
        #Scrapes the player position
        elif type == "position":
            position = tabletext.text.strip() #Extracts text from table row element
            position = derive_position(position) #Translates FW to forward or DF to defender

         #Scrapes the Player's Team
        elif type == "team":
            team = tabletext.find('a') #Looks for team hyperlink
            team = team.text.strip() #Retrieves hyperlink text as team name
            team = str(team)
    
        #Scrapes the player age
        elif type == "age":
            age = tabletext.text.strip() #Retrieves age code
            age = age[:2] #Takes necessary first 2 digits of the age

        #Scrapes the amount of games played
        elif type == "games":
            games = tabletext.text.strip() #Extracts amount of games as text from tr
            games = str(games)
        
        #Scrapes the amount of minutes played
        elif type == "minutes":
            minutes = tabletext.text.strip() #Extracts amount of minutes played
            minutes = str(minutes)
        
        #Scrapes amount of goals scored
        elif type == "goals":
            goals = tabletext.text.strip() #Extracts amount of goals scored
            goals = str(goals)

        #Scrapes amount of assists
        elif type == "assists":
            assists = tabletext.text.strip() #Extracts amount of assists
            assists = str(assists)

        #Scrapes G/A
        elif type == "goals_assists":
            goal_assists = tabletext.text.strip() #Extracts G/A from td
            goal_assists = str(goal_assists)

        #Scrapes Yellow Cards
        elif type == "cards_yellow":
            yellow_cards = tabletext.text.strip() #Extracts yellow card count from td
            yellow_cards = str(yellow_cards)
        
        #Scrapes Red cards
        elif type == "cards_red":
            red_cards = tabletext.text.strip() #Extracts red card count from td
            red_cards = str(red_cards)
    
    #Stores each value in csv file
    storefile(player_name, nationality, position, team, age, games, minutes, goals, assists, goal_assists, yellow_cards, red_cards)
    