# Shane's Olympic Rankings
# Contains a function to calculate the rankings, sets up and conducts web scraping to populate the countries variable

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

#output a list with name and score
    list = [(country['name'], country['score']) for country in ranked_countries]

return list

#install library for web scraping
!pip install beautifulsoup4

#conduct web scraping
import requests
from bs4 import BeautifulSoup

def get_medal_data(url):
    response = requests.get(url)
    if response.status_code != 200
        print("Failed to retrieve the webpage")
        return []
        
    soup = BeautifulSoup(response.content,'html.parser')
    table = soup.find('table') #may need to adjust based on olympics page
    countries = []
    
    #Assuming the table has the structure with country names and medal counts in specific columns
    for row in table.find_all('tr')[1:]: #skips header row
        cells = row.find_all('td')
        if len(cells) < 4:
            continue
        country = {'name':cells[0].get_text(strip=True),'gold':int(cells[1].get_text(strip=True)),'silver':int(cells[2].get_text(strip=True)),'bronze':int(cells[3].get_text(strip=True))}
        countries.append(country)
        
return countries

#Test the functions
url = 'https://olympics.com/en/paris-2024/medals'
countries = get_medal_data(url)
print olympics(countries)




