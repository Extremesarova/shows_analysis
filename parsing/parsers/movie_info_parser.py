import re
from typing import Tuple

from bs4 import BeautifulSoup


class MovieInfoParser:
    MOVIE_URL_TEMP = "https://www.kinopoisk.ru/film/"

    def __init__(self, movie_soup: BeautifulSoup):
        self.movie_dict = {}
        self.movie_soup = movie_soup

    def get_id(self) -> str:
        movie_id = self.movie_soup.find_all("link", attrs={"href": re.compile(self.MOVIE_URL_TEMP)})[0]
        movie_id = movie_id["href"].split("/")[-2]
        return movie_id

    def get_names(self) -> Tuple[str, str]:
        movie_name: str = self.movie_soup.find_all("h1", attrs={"class": re.compile("styles_title")})[0].get_text()
        movie_name_original: str = \
            self.movie_soup.find_all("span", attrs={"class": re.compile("styles_originalTitle")})[
                0].get_text()

        return movie_name, movie_name_original
