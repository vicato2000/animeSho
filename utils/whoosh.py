import os
import shutil

from whoosh.fields import Schema, TEXT, NUMERIC, KEYWORD, DATETIME, ID
from whoosh.index import create_in, open_dir
from whoosh.qparser import MultifieldParser

from main import models

schema_anime = Schema(
    id = TEXT(stored=True),
    title=TEXT(stored=True),
    synopsis=TEXT(stored=True),
    episodes=NUMERIC(stored=True),
    type=KEYWORD(stored=True),
    studios=KEYWORD(stored=True),
    genres=KEYWORD(stored=True),
    date_start=DATETIME(stored=True),
    date_end=DATETIME(stored=True),
)


def create_index():
    if os.path.exists("index"):
        shutil.rmtree("index")
    os.mkdir("index")

    ix = create_in("index", schema_anime)
    writer = ix.writer()
    for anime in models.Anime.objects.all():

        date_start = anime.date_start
        date_end = anime.date_end

        if date_start:
            date_start = date_start.strftime("%Y-%m-%d")
        if date_end:
            date_end = date_end.strftime("%Y-%m-%d")

        writer.add_document(
            id=anime.id.__str__(),
            title=anime.title,
            synopsis=anime.synopsis,
            episodes=anime.episodes,
            type=anime.type.name,
            studios=','.join([studio.name for studio in anime.studios.all()]),
            genres=','.join([genre.name for genre in anime.genres.all()]),
            date_start=date_start,
            date_end=date_end,
        )
    writer.commit()


def general_search(query):
    ix = open_dir("index")
    with ix.searcher() as searcher:
        query = MultifieldParser(['title', 'synopsis', 'studios', 'genres'], ix.schema).parse(query)
        results = searcher.search(query)
        results = [models.Anime.objects.get(id=int(result['id'])) for result in results]
        return results
