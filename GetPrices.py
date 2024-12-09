from bs4 import BeautifulSoup
import requests
import concurrent.futures


def build_title_for_div(title):
    return title.replace("'", "")\
                .replace("!", "") \
                .replace(" & ", " ") \
                .replace(" ", "-") \
                .replace("#", "") \
                .replace(".", "") \
                .replace("+", "") \
                .replace("?", "")


def get_gg_deals_soup(url):
    page = requests.get(url)
    return BeautifulSoup(page.content, "html.parser")
    

def find_game_from_soup(soup, title):
    return soup.find('div', {"data-game-name": title})

def get_price_from_game(game):
    return game.find('span', {"class": "price-inner numeric"}).get_text().replace("~", "")

def get_price(title):
    price = "No Price Found"
    formattedTitle = title.lower().replace(":", "")
    titleForURL = formattedTitle.replace("'", "%27").replace(" ", "+")
    titleForDiv = build_title_for_div(formattedTitle)
    
    URL = 'https://gg.deals/games/?title={}'.format(titleForURL)
    
    try:
        soup = get_gg_deals_soup(URL)
        game = find_game_from_soup(soup, titleForDiv)
        price = get_price_from_game(game)
    except AttributeError:
        print('Could not retrieve pricing information for {}'.format(title))
    
    return title, price

def buildCsv(titles):
    data = [
            ['Title', 'Price']
        ]

    with concurrent.futures.ThreadPoolExecutor(20) as executor:
        results = executor.map(get_price, titles)
        for result in results:
            data.append(result)
    
    try: 
        csv_file_path = 'games.csv'
        with open (csv_file_path, mode='w') as file:
            for row in data:
                file.write(','.join(map(str, row)) + '\n')
    except AttributeError:
        print('Error creating CSV')



gamesList = ["112 Operator", "911 Operator", "Stick Fight: The Game"]
buildCsv(gamesList)
