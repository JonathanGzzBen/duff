from typing import List
from urllib.request import urlopen
from bs4 import BeautifulSoup
import operator


class Anime:
    title: str
    score: str
    studio: str
    episodes: str
    image_url: str


def animes_season(limit: int = 0) -> List[Anime]:
    try:
        html = urlopen("https://myanimelist.net/anime/season")
        bs = BeautifulSoup(html.read(), 'html.parser')
        animes = []
        animes_seasonal = bs.find_all(
            "div", {"class": "seasonal-anime js-seasonal-anime"})
        animes_added = 0
        for seasonal_anime in animes_seasonal:
            anime = Anime()
            anime.title= seasonal_anime.find("h2", {"class": "h2_anime_title"}).a.get_text()
            anime.studio = seasonal_anime.find("span", {"class": "producer"}).get_text().strip()
            anime.score = (seasonal_anime.find("span", {"class": "score"}).get_text().strip())
            anime.episodes = seasonal_anime.find("div", {"class": "eps"}).get_text().strip()

            image_url= ""
            try:
                image_url =  seasonal_anime.find("div", {"class": "image"}).a.img["src"]
                if image_url == "":
                    image_url = seasonal_anime.find("div", {"class": "image"}).a.img["data-src"]
            except:
                image_url = ""
            anime.image_url = image_url
                
            animes.append(anime)
            animes_added += 1
            if limit != 0 and animes_added >= limit:
                return animes
        return animes
    except:
        return []


if __name__ == "__main__":
    seasonal_animes = animes_season(limit=5)
    for anime in seasonal_animes:
        print(anime.title)