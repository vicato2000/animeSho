import requests
import re
from bs4 import BeautifulSoup

ANIME_URL = 'https://myanimelist.net/topanime.php?limit='


def get_animes_hrefs() -> list[str]:
    """
    Obetener los enlaces de los 1000 animes mas populares de MyAnimeList
    """

    anime_list = []

    for i in range(0, 1000, 50):
        url = ANIME_URL + str(i)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'lxml')

        hrefs = soup.find_all('a', class_=['hoverinfo_trigger'])

        anime_list.extend([href['href'] for href in hrefs])

    return anime_list


def get_anime_info():
    hrefs = get_animes_hrefs()

    for href in hrefs:
        page = requests.get(href)
        soup = BeautifulSoup(page.content, 'lxml')

        title = soup.find('h1', class_=['title-name']).strong.text
        image = soup.find('img', class_=['lazyloaded'])['data-src']
        synopsis = soup.find('p', itemprop='description').text
        score = soup.find('div', class_=['score-label']).text
        rank = soup.find('span', class_='numbers ranked').strong.text.replace('#', '')
        popularity = soup.find('span', class_='numbers popularity').strong.text.replace('#', '')
        type = soup.find('span', text=re.compile('Type:')).find_next('a').text
        episodes = soup.find('span', text=re.compile('Episodes:')).next_sibling.text.strip()
        status = soup.find('span', text=re.compile('Status:')).next_sibling.text.strip()
        studios = soup.find('span', text=re.compile('Studios:')).find_next('a').text




if __name__ == '__main__':
    get_anime_info()
