from bs4 import BeautifulSoup
import requests


def getPrice(title):
    price = "No Price Found"
    formattedTitle = title.lower().replace(":", "")
    titleForURL = formattedTitle.replace("'", "%27").replace(" ", "+")
    titleForDiv = formattedTitle.replace("'", "-").replace(" ", "-")
    URL = 'https://gg.deals/games/?title={}'.format(titleForURL)
    
    try:
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        game = soup.find('div', {"data-game-name": titleForDiv})
        price = game.find('span', {"class": "price-inner numeric"}).get_text()
    except AttributeError:
        print('Could not retrieve pricing information for {}'.format(title))
    
    return price

def buildCsv(titles):
    data = [
            ['Title', 'Price']
        ]
    for title in titles:
        price = getPrice(title)
        data.append([title, price])
    
    
    try: 
        csv_file_path = 'games.csv'
        with open (csv_file_path, mode='w') as file:
            for row in data:
                file.write(','.join(map(str, row)) + '\n')
    except AttributeError:
        print('Error creating CSV')



gamesList = []
buildCsv(gamesList)
