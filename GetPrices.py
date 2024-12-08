from bs4 import BeautifulSoup
import requests

gamesList = []

def getPrice(title):
    formattedTitle = title.lower().replace(":", "")
    titleForURL = formattedTitle.replace("'", "%27").replace(" ", "+")
    titleForDiv = formattedTitle.replace("'", "-").replace(" ", "-")
    URL = 'https://gg.deals/games/?title={}'.format(titleForURL)
    
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    game = soup.find('div', {"data-game-name": titleForDiv})
    price = game.find('span', {"class": "price-inner numeric"}).get_text()
    
    return price

for game in gamesList:
    try:
        print("{}: {}".format(game, getPrice(game)))
    except AttributeError:
        print('Could not retrieve pricing information for {}'.format(game))



