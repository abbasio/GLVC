from bs4 import BeautifulSoup
import requests
import concurrent.futures


def get_price(title):
    price = "No Price Found"
    formattedTitle = title.lower().replace(":", "")
    titleForURL = formattedTitle.replace("'", "%27").replace(" ", "+")
    titleForDiv = formattedTitle.replace("'", "") \
                                .replace("!", "") \
                                .replace(" & ", " ") \
                                .replace(" ", "-") \
                                .replace("#", "") \
                                .replace(".", "") \
                                .replace("+", "") \
                                .replace("?", "")
    
    URL = 'https://gg.deals/games/?title={}'.format(titleForURL)
    
    try:
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, "html.parser")
        game = soup.find('div', {"data-game-name": titleForDiv})
        price = game.find('span', {"class": "price-inner numeric"}).get_text()
    except AttributeError:
        print('Could not retrieve pricing information for {}'.format(title))
    
    return title, price.replace("~", "")

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
