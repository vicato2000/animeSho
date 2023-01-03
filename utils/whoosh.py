import os
import shutil

from whoosh.fields import Schema, TEXT, NUMERIC, KEYWORD, DATETIME, ID
from whoosh.index import create_in, open_dir
from whoosh.qparser import MultifieldParser, QueryParser, SequencePlugin, PhrasePlugin
from whoosh.analysis import StemmingAnalyzer
from whoosh.query import Phrase

from main import models

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

        date_start = anime.date_start
        date_end = anime.date_end

        if date_start:
            date_start = date_start.strftime("%Y-%m-%d")
        if date_end:
            date_end = date_end.strftime("%Y-%m-%d")

        writer.add_document(
            id=anime.id.__str__(),
            title=anime.title.lower(),
            synopsis=anime.synopsis.lower(),
            episodes=anime.episodes,
            type=anime.type.name.lower(),
            studios=','.join([studio.name.lower() for studio in anime.studios.all()]),
            genres=','.join([genre.name.lower() for genre in anime.genres.all()]),
            date_start=date_start,
            date_end=date_end,
        )
    writer.commit()


def general_search(query):
    ix = open_dir("index")
    with ix.searcher() as searcher:
        query = MultifieldParser(['title', 'synopsis', 'studios', 'genres'], ix.schema).parse(query.lower())
        results = searcher.search(query)
        results = [models.Anime.objects.get(id=int(result['id'])) for result in results]
        return results


def phrase_search(phrase):
    ix = open_dir("index")
    with ix.searcher() as searcher:
        # phrase = [u'{}'.format(p) for p in phrase.lower().strip().split(' ')]
        query = QueryParser("synopsis", ix.schema).parse(phrase)
        results = searcher.search(query)
        results = [models.Anime.objects.get(id=int(result['id'])) for result in results]
        return results
