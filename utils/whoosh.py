import os
import shutil

from whoosh.fields import Schema, TEXT, NUMERIC, KEYWORD, DATETIME
from whoosh.index import create_in, open_dir
from whoosh.qparser import MultifieldParser, QueryParser
from whoosh.analysis import StemmingAnalyzer

from main import models

from datetime import datetime

schema_anime = Schema(
    id=TEXT(stored=True),
    title=TEXT(stored=True),
    synopsis=TEXT(stored=True, analyzer=StemmingAnalyzer()),
    episodes=NUMERIC(stored=True),
    type=KEYWORD(stored=True, commas=True),
    studios=KEYWORD(stored=True, commas=True),
    genres=KEYWORD(stored=True, commas=True),
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
        writer.add_document(
            id=anime.id.__str__(),
            title=anime.title.lower(),
            synopsis=anime.synopsis.lower(),
            episodes=anime.episodes,
            type=anime.type.name.lower(),
            studios=','.join([studio.name.lower() for studio in anime.studios.all()]),
            genres=','.join([genre.name.lower() for genre in anime.genres.all()]),
            date_start=anime.date_start.strftime("%Y%m%d") if anime.date_start else None,
            date_end=anime.date_end.strftime("%Y%m%d") if anime.date_end else None,
        )
    writer.commit()


def general_search(query):
    ix = open_dir("index")
    with ix.searcher() as searcher:
        query = MultifieldParser(['title', 'synopsis', 'studios', 'genres'], ix.schema).parse(query.lower())
        results = searcher.search(query, limit=None)
        results = [models.Anime.objects.get(id=int(result['id'])) for result in results]
        return results


def phrase_search(phrase):
    ix = open_dir("index")
    with ix.searcher() as searcher:
        query = QueryParser("synopsis", ix.schema).parse(phrase)
        results = searcher.search(query, limit=12)
        results = [models.Anime.objects.get(id=int(result['id'])) for result in results]
        return results


def date_search(date_start=None, date_end=None):
    ix = open_dir("index")

    with ix.searcher() as searcher:

        if not date_end:
            date_start = datetime.strptime(date_start, "%Y-%m-%d").strftime("%Y%m%d")
            query = QueryParser("date_start", ix.schema).parse(f'[{date_start} TO]')
            results = searcher.search(query, limit=None)
            results = [models.Anime.objects.get(id=int(result['id'])) for result in results]

            results = sorted(results, key=lambda x: x.date_start)

            return results
        elif not date_start:
            date_end = datetime.strptime(date_end, "%Y-%m-%d").strftime("%Y%m%d")
            query = QueryParser("date_end", ix.schema).parse(f'[TO {date_end}]')
            results = searcher.search(query, limit=None)
            results = [models.Anime.objects.get(id=int(result['id'])) for result in results]

            results = sorted(results, key=lambda x: x.date_end)

            return results
        else:
            date_start = datetime.strptime(date_start, "%Y-%m-%d").strftime("%Y%m%d")
            date_end = datetime.strptime(date_end, "%Y-%m-%d").strftime("%Y%m%d")
            query = QueryParser("date_start", ix.schema).parse(f'[{date_start} TO {date_end}]')
            query2 = QueryParser("date_end", ix.schema).parse(f'[{date_start} TO {date_end}]')
            results = searcher.search(query, limit=None)
            results = [models.Anime.objects.get(id=int(result['id'])) for result in results]
            results2 = searcher.search(query2, limit=None)
            results2 = [models.Anime.objects.get(id=int(result['id'])) for result in results2]

            result = sorted(list(set(results).intersection(results2)), key=lambda x: x.date_start)

            return result


def episodes_search(number, operator):
    ix = open_dir("index")
    with ix.searcher() as searcher:
        if operator == 'g':
            query = QueryParser("episodes", ix.schema).parse(f'[{number} TO]')
        else:
            query = QueryParser("episodes", ix.schema).parse(f'[TO {number}]')
        results = searcher.search(query, limit=None)
        results = [models.Anime.objects.get(id=int(result['id'])) for result in results]

        if operator == 'g':
            results = sorted(results, key=lambda x: x.episodes)
        else:
            results = sorted(results, key=lambda x: x.episodes, reverse=True)

        return results




