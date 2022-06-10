from bs4 import BeautifulSoup

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
        self.series_info = self.get_show_info()
