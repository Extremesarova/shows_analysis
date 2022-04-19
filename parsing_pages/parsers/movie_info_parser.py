import re

from bs4 import BeautifulSoup

from parsing_pages.dataclasses.movie_info import MovieId, MovieTitles, MovieCast, MovieInfo
from parsing_pages.preprocessing.preprocessor import Preprocessor


class MovieInfoParser:
    MOVIE_URL_TEMP = "https://www.kinopoisk.ru/film/"
    TITLES_MAP = {'Год производства': "year",
                  'Страна': "country",
                  'Жанр': "genre",
                  'Слоган': "slogan",
                  'Режиссер': "director",
                  'Сценарий': "scriptwriter",
                  'Продюсер': "producer",
                  'Оператор': "operator",
                  'Композитор': "composer",
                  'Художник': "artist",
                  'Монтаж': "cut",
                  'Бюджет': "budget",
                  'Маркетинг': "marketing",
                  'Сборы в США': "us_box_office",
                  'Сборы в мире': "world_box_office",
                  'Зрители': "viewers",
                  'Сборы в России': "russian_box_office",
                  'Премьера в Росcии': "russian_premiere",
                  'Премьера в мире': "world_premiere",
                  'Релиз на DVD': "dvd_release",
                  'Релиз на Blu-ray': "blue_ray_release",
                  'Возраст': "age_rating",
                  'Рейтинг MPAA': "mpaa_rating",
                  'Время': "duration"
                  }

    def __init__(self, movie_soup: BeautifulSoup):
        self.movie_soup = movie_soup
        self.preprocessor = Preprocessor()
        self.movie_dict = {}

        # self.movie_info = MovieInfo()

    def get_id(self) -> MovieId:
        id = self.movie_soup.find_all("link", attrs={"href": re.compile(self.MOVIE_URL_TEMP)})[0]
        id = int(id["href"].split("/")[-2])
        return MovieId(id=id)

    def get_titles(self) -> MovieTitles:
        # TODO preprocess values
        russian_title: str = self.movie_soup.find_all("h1", attrs={"class": re.compile("styles_title")})[0].get_text()
        original_title: str = \
            self.movie_soup.find_all("span", attrs={"class": re.compile("styles_originalTitle")})[
                0].get_text()

        return MovieTitles(russian_title, original_title)

    def get_actors(self) -> MovieCast:
        actors_soup_tag, voice_actors_tag = [tag_ for tag_ in
                                             self.movie_soup.find_all("ul", attrs={"class": re.compile("styles_list")})]

        actors = [actor.get_text() for actor in
                  actors_soup_tag.find_all("a", attrs={"class": re.compile("styles_link")})]

        voice_actors = [actor.get_text() for actor in
                        voice_actors_tag.find_all("a", attrs={"class": re.compile("styles_link")})]

        return MovieCast(actors, voice_actors)

    def get_info(self) -> MovieInfo:
        # TODO preprocess values
        movie_info_divs = self.movie_soup.find_all("div", attrs={"data-test-id": re.compile("encyclopedic-table")})[0]

        values = []
        for div in movie_info_divs.find_all(
                "div", attrs={"class": re.compile("styles_value"), "data-tid": re.compile(".*")}
        ):
            current_value = div.get_text().replace("сборы", "")
            if "слова" not in current_value:
                values.append(current_value)

        titles = []
        for div in movie_info_divs.find_all(class_=re.compile("styles_title")):
            current_title = div.get_text()
            titles.append(current_title)

        assert len(values) == len(titles)

        titles_en = [self.TITLES_MAP.get(title, "") for title in titles]
        info_dict = dict(zip(titles_en, values))

        return MovieInfo(**info_dict)