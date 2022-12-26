from typing import Tuple, List, Set

import requests
import multiprocessing
from multiprocessing import Pool
import re
import tqdm
from bs4 import BeautifulSoup
from dataclasses import dataclass

ANIME_URL = 'https://myanimelist.net/topanime.php?limit='


@dataclass
class Anime:
    """
    Representación de un anime.

    Attributes:
        title (str): Título del anime.
        image (str): URL de la imagen del anime.
        synopsis (str): Sinopsis del anime.
        score (float): Puntuación del anime.
        rank (int): Posición del anime en la lista.
        popularity (int): Popularidad del anime.
        type (str): Tipo de anime.
        episodes (int): Número de episodios del anime.
        status (str): Estado del anime.
        studios (str): Estudiosque produjo el anime.
        genres (str): Géneros del anime.

    """

    title: str
    image: str
    synopsis: str
    score: float
    rank: int
    popularity: int
    type: str
    episodes: int
    status: str
    studios: list[str]
    genres: list[str]

    def __str__(self):
        return f'{self.title} - {self.score} - {self.rank} - {self.popularity} - {self.type} - {self.episodes} - {self.status} - {self.studios} - {self.genres}'


def get_animes_hrefs() -> list[str]:

    """
    Obetener los enlaces de los 1000 animes mas populares de MyAnimeList

    Returns:
        list[str]: Lista de enlaces de los 1000 animes mas populares de MyAnimeList
    """

    anime_list = []

    for i in range(0, 1000, 50):
        url = ANIME_URL + str(i)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'lxml')

        hrefs = soup.find_all('a', class_=['hoverinfo_trigger'])

        anime_list.extend([href['href'] for href in hrefs])

    return anime_list


def anime_info(href) -> tuple[Anime, str, str, list[str], list[str]]:

    """
    Obtener la informacion de un anime

    Args:
        href (str): Enlace del anime
    Returns:
        tuple[Anime, str, str, list[str], list[str]]: Tupla con la informacion del anime
    """

    page = requests.get(href)
    soup = BeautifulSoup(page.content, 'lxml')

    title = soup.find('h1', class_=['title-name']).strong.text
    for rex in ['lazyloaded', 'lazyload']:
        image = soup.find('img', class_=rex)
        if image:
            image = image['data-src']
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

    return Anime(title, image, synopsis, float(score), int(rank), int(popularity), type,
                 0 if episodes == 'Unknown' else int(episodes), status, studios, genres), type, status, studios, genres


def get_anime_info() -> tuple[list[Anime], set[str], set[str] | str, set[str] | list[str], set[str] | list[str]]:

    """
    Obtener la informacion de los 1000 animes mas populares de MyAnimeList, haciendo uso de multiprocessing para
    acelerar el proceso de scraping.

    Returns:
        tuple[list[Anime], set[str], set[str] | str, set[str] | list[str], set[str] | list[str]]: Tupla con la
        informacion necesaria para cargar la base de datos.
    """

    hrefs = get_animes_hrefs()

    with Pool(processes=multiprocessing.cpu_count()*16) as pool, tqdm.tqdm(total=len(hrefs)) as pbar:
        animes = []
        types_ = set()
        status_ = set()
        studios_ = set()
        genres_ = set()
        for anime, type, status, studios, genres in pool.imap_unordered(anime_info, hrefs):
            animes.append(anime)
            types_.add(type)
            status_.add(status)
            studios_.update(studios)
            genres_.update(genres)
            pbar.update()

    return animes, types_, status_, studios_, genres_


if __name__ == '__main__':
    for a in get_anime_info()[0]:
        print(a)

