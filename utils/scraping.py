import requests
import multiprocessing
import re
import tqdm
from bs4 import BeautifulSoup
from dataclasses import dataclass

ANIME_URL = 'https://myanimelist.net/topanime.php?limit='


@dataclass
class Anime:
    title: str
    image: str
    synopsis: str
    score: str
    rank: str
    popularity: str
    type: str
    episodes: str
    status: str
    studios: list[str]
    genres: list[str]


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


def anime_info(href):
    page = requests.get(href)
    soup = BeautifulSoup(page.content, 'lxml')

    title = soup.find('h1', class_=['title-name']).strong.text
    for rex in ['lazyload', 'lazyloaded']:
        image = soup.find('img', class_=rex)
        if image:
            image = image.src
            break
    synopsis = soup.find('p', itemprop='description').text
    score = soup.find('div', class_=['score-label']).text
    rank = soup.find('span', class_='numbers ranked').strong.text.replace('#', '')
    popularity = soup.find('span', class_='numbers popularity').strong.text.replace('#', '')
    type = soup.find('span', text=re.compile('Type:')).find_next('a').text
    episodes = soup.find('span', text=re.compile('Episodes:')).next_sibling.text.strip()
    status = soup.find('span', text=re.compile('Status:')).next_sibling.text.strip()
    studios = soup.find('span', text=re.compile('Studios:')).parent.find_all('a')
    studios = [studio.text for studio in studios]
    genres = []
    for rex in ['Genres:', 'Genre:']:
        g = soup.find('span', text=re.compile(rex))
        if g:
            g2 = g.parent.find_all('a')
            genres.extend([genre.text for genre in g2])
            break

    anime = Anime(title, image, synopsis, score, rank, popularity, type, episodes, status, studios, genres)

    animates = [anime]

    return animates


def get_anime_info():

    hrefs = get_animes_hrefs()

    # for href in hrefs:
    #     page = requests.get(href)
    #     soup = BeautifulSoup(page.content, 'lxml')
    #
    #     title = soup.find('h1', class_=['title-name']).strong.text
    #     print(f'{i} - {title}')
    #     image = soup.find('img', class_='lazyloaded').src
    #     synopsis = soup.find('p', itemprop='description').text
    #     score = soup.find('div', class_=['score-label']).text
    #     rank = soup.find('span', class_='numbers ranked').strong.text.replace('#', '')
    #     popularity = soup.find('span', class_='numbers popularity').strong.text.replace('#', '')
    #     type = soup.find('span', text=re.compile('Type:')).find_next('a').text
    #     episodes = soup.find('span', text=re.compile('Episodes:')).next_sibling.text.strip()
    #     status = soup.find('span', text=re.compile('Status:')).next_sibling.text.strip()
    #     studios = soup.find('span', text=re.compile('Studios:')).parent.find_all('a')
    #     studios = [studio.text for studio in studios]
    #     genres = []
    #     for rex in ['Genres:', 'Genre:']:
    #         g = soup.find('span', text=re.compile(rex))
    #         if g:
    #             g2 = g.parent.find_all('a')
    #             genres.extend([genre.text for genre in g2])
    #             break
    #
    #     anime = Anime(title, image, synopsis, score, rank, popularity, type, episodes, status, studios, genres)
    #
    #     result.append(anime)
    #     i+=1

    with multiprocessing.Pool(processes=multiprocessing.cpu_count()*2) as pool, tqdm.tqdm(total=len(hrefs)) as pbar:
        all_data = []
        for data in pool.imap_unordered(anime_info, hrefs):
            all_data.extend(data)
            pbar.update()

    return all_data


if __name__ == '__main__':
    print(len(get_anime_info()))

