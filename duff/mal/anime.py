from typing import List
from urllib.request import urlopen
import urllib.parse
from bs4 import BeautifulSoup


class Anime:
    title: str
    score: str
    studio: str
    episodes: str
    image_url: str
    broadcast: str


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

def search_anime(anime_search: str) -> Anime:
    try:
        anime_search_url = ("https://myanimelist.net/anime.php?q={0}&cat=anime"
            .format(urllib.parse.quote(anime_search)))
        anime_search_html = urlopen(anime_search_url)
        bsAnimeSearchPage = BeautifulSoup(anime_search_html.read(), 'html.parser')
        anime_url = bsAnimeSearchPage.find("div", {"class": "js-categories-seasonal"}).table.find_all("tr")[1].a["href"]
        anime_page_html = urlopen(anime_url)
        bsAnimePage = BeautifulSoup(anime_page_html.read(), "html.parser")
        anime = Anime()
        anime.title = bsAnimePage.find("h1", {"class": "title-name"}).get_text().strip()
        anime.score = bsAnimePage.find("div", {"class": "score-label"}).get_text().strip()
        anime.image_url = bsAnimePage.find("td", {"class": "borderClass"}).div.div.a.img["data-src"].strip()
        infos_headers = bsAnimePage.find_all("span", {"class": "dark_text"})
        for header in infos_headers:
            header_text = header.get_text().strip()
            if header_text == "Episodes:":
                episodes_container = header.parent
                header.extract()
                anime.episodes = episodes_container.get_text().strip()
            elif header_text == "Broadcast:":
                broadcast_container = header.parent
                header.extract()
                anime.broadcast = broadcast_container.get_text().strip()
            elif header_text == "Studios:":
                studios_container = header.parent
                header.extract()
                anime.studio = studios_container.get_text().strip()
        return anime
    except:
        return None

if __name__ == "__main__":
    seasonal_animes = animes_season(limit=5)
    for anime in seasonal_animes:
        print(anime.title)