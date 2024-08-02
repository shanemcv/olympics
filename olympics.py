# Shane's Olympic Rankings
# Contains a function to calculate the rankings, pull html content from wikipedia using their api and parse the medal table

#this function calculates my ranking and ouputs a list
def olympic(countries):

#define value for each medal
    bronze_value = 1
    silver_value = 2
    gold_value = 4

#calculate the ranking score based on above values
    for country in countries:
        country['score'] = country['gold'] * gold_value + country['silver'] * silver_value + country['bronze'] * bronze_value
        
#sort the countries in descending order by score
    ranked_countries = sorted(countries, key=lambda x:x['score'], reverse=True)

# Add rank to each country
    for rank, country in enumerate(ranked_countries, start=1):
        country['rank'] = rank

#output a list with name and score
    list = [(country['rank'], country['country'], country['score']) for country in ranked_countries]

    return list

#set up wikipedia api and csv imports
import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime

#this function pulls the html of a specific section of a wikipedia page using the wikipedia api
def fetch_html(title,section):
    url = 'https://en.wikipedia.org/w/api.php'
    params = {
        'action': 'parse',
        'page': title,
        'section': section,
        'format': 'json'
    }
    session = requests.Session()
    response = session.get(url=url, params=params)
    data = response.json() #Attempt to parse json
    return data['parse']['text']['*'] 

#this function parses the table from the wikipedia page
def parse_medal_table(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    table = soup.find('table', class_='wikitable')

    results = []
    for row in table.find_all('tr')[1:]: #this skips the header row
        cells = row.find_all(['th', 'td'])
        if len(cells) < 6:
            continue
        original_rank = cells[0].get_text(strip=True)
        country = cells[1].get_text(strip=True)
        gold = int(cells[2].get_text(strip=True))
        silver = int(cells[3].get_text(strip=True))
        bronze = int(cells[4].get_text(strip=True))
        total = int(cells[5].get_text(strip=True))
        results.append({
            'original rank': original_rank,
            'country': country,
            'gold': gold,
            'silver': silver,
            'bronze': bronze,
            'total': total
        })

    return results

#this function creates a csv file with today's date and my rankings
def save_to_csv(list, base_filename="Shane's Olympic Rankings"):
    #Get current date
    today_date = datetime.now().strftime('%Y-%m-%d')

    #create filename with current date
    filename = f"{base_filename}_{today_date}.csv"

    with open(filename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Rank', 'Country', 'Score']) #header row
        writer.writerows(list)

    print(f"File saved successfully to {filename}")

#Test the functions
title = '2024_Summer_Olympics_medal_table'
section = 2

html_content = fetch_html(title,section)
countries = parse_medal_table(html_content)
list = olympic(countries)

''' 

You can use the following code to print the rankings instead of saving to csv

for rank,country,score in list:
    print(f"{rank}: {country}: {score}\n")

'''

save_to_csv(list)