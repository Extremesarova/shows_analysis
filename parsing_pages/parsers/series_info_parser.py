import re

from bs4 import BeautifulSoup

from parsing_pages.dataclasses.show_info import SeriesInfo, from_dict_to_dataclass
from parsing_pages.parsers.show_info_parser import ShowInfoParser


class SeriesInfoParser(ShowInfoParser):
    SHOW_URL_TEMP = "https://www.kinopoisk.ru/series/"
    TITLES_MAP = {"Год производства": "year",
                  "Страна": "country",
                  "Жанр": "genre",
                  "Слоган": "slogan",
                  "Режиссер": "director",
                  "Сценарий": "scriptwriter",
                  "Продюсер": "producer",
                  "Оператор": "operator",
                  "Композитор": "composer",
                  "Художник": "artist",
                  "Монтаж": "cut",
                  "Бюджет": "budget",
                  "Сборы в США": "us_box_office",
                  "Сборы в мире": "world_box_office",
                  "Сборы в России": "russian_box_office",
                  "Премьера в Росcии": "russian_premiere",
                  "Премьера в мире": "world_premiere",
                  "Релиз на DVD": "dvd_release",
                  "Релиз на Blu-ray": "blue_ray_release",
                  "Возраст": "age_rating",
                  "Рейтинг MPAA": "mpaa_rating",
                  "Время": "duration",
                  "Цифровой релиз": "digital_release",
                  "Платформа": "platform",
                  "Директор фильма": "film_director"
                  }

    def __init__(self, series_soup: BeautifulSoup):
        super().__init__(series_soup)
        self.show_info = self.get_show_info()

    def get_info(self) -> SeriesInfo:
        # TODO preprocess values
        movie_info_divs = self.show_soup.find_all("div", attrs={"data-test-id": re.compile("encyclopedic-table")})[0]
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

        info_dict["year"] = info_dict["year"]
        info_dict["slogan"] = info_dict["slogan"] if info_dict["slogan"] != "—" else self.NA_TAG

        return from_dict_to_dataclass(SeriesInfo, info_dict)
