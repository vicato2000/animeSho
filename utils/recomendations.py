from main import models


def dice_coefficient(set1, set2):
    return 2 * len(set1.intersection(set2)) / (len(set1) + len(set2))


def get_recommendations(anime):
    recommendations = []
    for anime2 in models.Anime.objects.all():
        if anime2 == anime:
            continue
        recommendations.append((anime2, dice_coefficient(anime.genres.all(), anime2.genres.all())))
    recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)
    return [x[0] for x in recommendations[:8]]


def get_recommendations_watchlist(user):
    recommendations = []

    watchlist = models.Watchlist.objects.filter(user=user).values_list('anime', flat=True)

    animes = models.Anime.objects.filter(id__in=watchlist)

    for anime in animes:
        r = []
        for anime2 in models.Anime.objects.all():
            if anime2 in animes:
                continue
            r.append((anime2, dice_coefficient(anime.genres.all(), anime2.genres.all())))
        recommendations.extend(r)

    recommendations = sorted(recommendations, key=lambda x: x[1], reverse=True)
    return [x[0] for x in recommendations[:36]]
