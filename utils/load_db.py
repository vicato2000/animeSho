import tqdm

from utils import scraping
from main import models
from multiprocessing import Pool
import multiprocessing


def load():
    delete_all()

    animes, types, status, studios, genres = scraping.get_anime_info()

    types = [models.Type(name=type) for type in types]
    models.Type.objects.bulk_create(types)

    status = [models.Status(name=status) for status in status]
    models.Status.objects.bulk_create(status)

    studios = [models.Studio(name=studio) for studio in studios]
    models.Studio.objects.bulk_create(studios)

    genres = [models.Genre(name=genre) for genre in genres]
    models.Genre.objects.bulk_create(genres)

    animes_ = []

    # with Pool() as pool, tqdm.tqdm(total=len(animes)) as pbar:
    #     for anime in pool.imap_unordered(save_anime, animes):
    #         animes.append(anime)
    #         pbar.update()

    for anime in tqdm.tqdm(animes):
        animes_.append(save_anime(anime))


    models.Anime.objects.bulk_create(animes_)


    animes_update = []

    for anime in tqdm.tqdm(animes):
        animes_update.append(complete_anime_info(anime))

    # models.Anime.objects.bulk_update(animes_update, ['studios', 'genres'])
    AnimeStudioRelation = models.Anime.studios.through
    AnimeGenreRelation = models.Anime.genres.through

    AnimeStudioRelation.objects.bulk_create([AnimeStudioRelation(anime_id=anime.id, studio_id=studio.id) for anime in animes_update for studio in anime.studios.all()])
    AnimeGenreRelation.objects.bulk_create([AnimeGenreRelation(anime_id=anime.id, genre_id=genre.id) for anime in animes_update for genre in anime.genres.all()])



def save_anime(anime: scraping.Anime):
    type = models.Type.objects.get(name=anime.type)
    status = models.Status.objects.get(name=anime.status)

    anime = models.Anime(title=anime.title, image=anime.image, synopsis=anime.synopsis, score=anime.score,
                         rank=anime.rank, popularity=anime.popularity, episodes=anime.episodes, type=type,
                         status=status)

    return anime


def complete_anime_info(anime: scraping.Anime):
    a = models.Anime.objects.get(rank=anime.rank)

    studios = models.Studio.objects.filter(name__in=anime.studios)
    genres = models.Genre.objects.filter(name__in=anime.genres)

    a.studios.set(studios)
    a.genres.set(genres)

    return a


def delete_all():
    models.Anime.objects.all().delete()
    models.Type.objects.all().delete()
    models.Status.objects.all().delete()
    models.Studio.objects.all().delete()
    models.Genre.objects.all().delete()


if __name__ == '__main__':
    load()
