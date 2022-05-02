import re

from bs4 import BeautifulSoup

from parsing_pages.dataclasses.movie_info import MovieId, Titles, Cast, MovieInfo, UserRating, Synopsis, \
    CriticsRating, MoviePage, from_dict_to_dataclass
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
                  'Цифровой релиз': "digital_release",
                  'Релиз на DVD': "dvd_release",
                  'Релиз на Blu-ray': "blue_ray_release",
                  'Возраст': "age_rating",
                  'Рейтинг MPAA': "mpaa_rating",
                  'Время': "duration"
                  }
    NA_TAG = "N/A"

    def __init__(self, movie_soup: BeautifulSoup):
        self.movie_soup = movie_soup
        self.preprocessor = Preprocessor()

        self.movie_info = MoviePage(id=self.get_id(),
                                    titles=self.get_titles(),
                                    cast=self.get_actors(),
                                    info=self.get_info(),
                                    user_rating=self.get_rating(),
                                    synopsis=self.get_synopsis(),
                                    critics_rating=self.get_critics_rating())

    @staticmethod
    def right_strip_trailing(original: str, trailing: str) -> str:
        trailing_len = len(trailing)
        if original[-trailing_len:] == trailing:
            return original[:-trailing_len]
        else:
            return original

    def get_id(self) -> MovieId:
        id = self.movie_soup.find_all("link", attrs={"href": re.compile(self.MOVIE_URL_TEMP)})[0]
        id = int(id["href"].split("/")[-2])
        return MovieId(id=id)

    def get_titles(self) -> Titles:
        # TODO preprocess values
        russian_title: str = self.movie_soup.find_all("h1", attrs={"class": re.compile("styles_title")})[0].get_text()
        original_title: str = \
            self.movie_soup.find_all("span", attrs={"class": re.compile("styles_originalTitle")})[
                0].get_text() if self.movie_soup.find_all("span",
                                                          attrs={"class": re.compile("styles_originalTitle")}) else ""

        return Titles(russian_title, original_title)

    def get_actors(self) -> Cast:
        actor_soups = [tag_ for tag_ in self.movie_soup.find_all("ul", attrs={"class": re.compile("styles_list")})]
        voice_actors_tag = None

        if len(actor_soups) == 2:
            actors_soup_tag, voice_actors_tag = actor_soups
        else:
            actors_soup_tag = actor_soups[0]

        actors = [actor.get_text() for actor in
                  actors_soup_tag.find_all("a", attrs={"class": re.compile("styles_link")})]

        if voice_actors_tag is not None:
            voice_actors = [actor.get_text() for actor in
                            voice_actors_tag.find_all("a", attrs={"class": re.compile("styles_link")})]
        else:
            voice_actors = []

        return Cast(actors, voice_actors)

    def get_info(self) -> MovieInfo:
        # TODO preprocess values
        movie_info_divs = self.movie_soup.find_all("div", attrs={"data-test-id": re.compile("encyclopedic-table")})[0]
        row_divs = movie_info_divs.find_all("div", attrs={"class": re.compile("styles_row")})
        values = []
        titles = []

        for row in row_divs:
            title = row.find("div", attrs={"class": re.compile("styles_title")}).get_text()
            value = row.find("div", attrs={"class": re.compile("styles_value")}).get_text()
            value = value[:-5] if value.endswith("слова") or value.endswith("сборы") else value
            titles.append(title)
            values.append(value)

        assert len(values) == len(titles)

        titles_en = [self.TITLES_MAP.get(title, "") for title in titles]

        info_dict: dict = dict(zip(titles_en, values))
        
        info_dict["year"] = int(info_dict["year"])
        info_dict["slogan"] = info_dict["slogan"] if info_dict["slogan"] != "—" else self.NA_TAG

        return from_dict_to_dataclass(MovieInfo, info_dict)

    def get_rating(self) -> UserRating:
        rating_imdb = ""
        rating_count_imdb = ""

        rating_kinopoisk = self.movie_soup.find_all("a", attrs={"class": re.compile("film-rating-value")}
                                                    )[0].get_text()

        rating_count_kinopoisk = self.movie_soup.find_all("span", attrs={"class": re.compile("styles_count")}
                                                          )[0].get_text()

        if self.movie_soup.find_all("span", attrs={"class": re.compile("styles_valueSection")}):
            rating_imdb = self.movie_soup.find_all("span", attrs={"class": re.compile("styles_valueSection")}
                                                   )[0].get_text()

            rating_count_imdb = self.movie_soup.find_all("div", attrs={"class": re.compile("film-sub-rating")}
                                                         )[0].find("span",
                                                                   attrs={
                                                                       "class": re.compile("styles_count")}).get_text()

        return UserRating(rating_kinopoisk, rating_count_kinopoisk, rating_imdb, rating_count_imdb)

    def get_synopsis(self) -> Synopsis:
        synopsis = self.movie_soup.find_all("div", attrs={"class": re.compile("styles_filmSynopsis")}
                                            )[0].get_text()

        return Synopsis(synopsis)

    def get_critics_rating(self) -> CriticsRating:
        russian_critics_percentage = ""
        russian_critics_number_of_reviews = ""
        world_critics_percentage = ""
        world_critics_star_value = ""
        world_critics_number_of_reviews = ""

        critics = self.movie_soup.find_all("div", attrs={"class": re.compile("styles_ratingBar")})

        if critics:
            world_critics = critics[0]
            if "в мире" in world_critics.get_text():
                world_critics_percentage = \
                    world_critics.find_all("span", attrs={"class": re.compile("film-rating-value")})[
                        0].get_text()
                world_critics_star_value = \
                    world_critics.find_all("span", attrs={"class": re.compile("styles_starValue")})[
                        0].get_text()

                world_critics_number_of_reviews_raw = \
                    world_critics.find_all("span", attrs={"class": re.compile("styles_count")})[
                        0].get_text()

                world_critics_number_of_reviews = self.right_strip_trailing(world_critics_number_of_reviews_raw,
                                                                            world_critics_star_value)

            if len(critics) >= 3:
                russian_critics = critics[2]

                russian_critics_percentage = \
                    russian_critics.find_all("span", attrs={"class": re.compile("film-rating-value")})[
                        0].get_text()

                russian_critics_number_of_reviews = \
                    russian_critics.find_all("span", attrs={"class": re.compile("styles_count")})[0].get_text()

        return CriticsRating(world_critics_percentage, world_critics_star_value, world_critics_number_of_reviews,
                             russian_critics_percentage, russian_critics_number_of_reviews)
