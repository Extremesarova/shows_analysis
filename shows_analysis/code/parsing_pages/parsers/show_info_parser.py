import re
from dataclasses import asdict

from bs4 import BeautifulSoup

from shows_analysis.parsing_pages.dataobjects.show_info import (Cast,
                                                                CriticsRating,
                                                                ShowId,
                                                                ShowPage,
                                                                Synopsis,
                                                                Titles,
                                                                UserRating)


class ShowInfoParser:
    SHOW_URL_TEMP = None
    TITLES_MAP = None
    NA_TAG = ""

    def __init__(self, show_soup: BeautifulSoup):
        self.show_soup = show_soup
        # self.preprocessor = Preprocessor()
        self.show_info = self.get_show_info()

    def get_info(self):
        raise NotImplementedError("Subclasses should implement this!")

    @staticmethod
    def right_strip_trailing(original: str, trailing: str) -> str:
        trailing_len = len(trailing)
        if original[-trailing_len:] == trailing:
            return original[:-trailing_len]
        else:
            return original

    def get_id(self) -> ShowId:
        id = self.show_soup.find_all(
            "link", attrs={"href": re.compile(self.SHOW_URL_TEMP)}
        )[0]
        id = int(id["href"].split("/")[-2])
        return ShowId(id=id)

    def get_titles(self) -> Titles:
        # TODO preprocess values
        russian_title: str = self.show_soup.find_all(
            "h1", attrs={"class": re.compile("styles_title")}
        )[0].get_text()
        original_title: str = (
            self.show_soup.find_all(
                "span", attrs={"class": re.compile("styles_originalTitle")}
            )[0].get_text()
            if self.show_soup.find_all(
                "span", attrs={"class": re.compile("styles_originalTitle")}
            )
            else ""
        )

        return Titles(russian_title, original_title)

    def get_actors(self) -> Cast:
        actor_soups = [
            tag_
            for tag_ in self.show_soup.find_all(
                "ul", attrs={"class": re.compile("styles_list")}
            )
        ]
        voice_actors_tag = None
        voice_actors = []
        actors = []

        if actor_soups:
            if len(actor_soups) == 2:
                actors_soup_tag, voice_actors_tag = actor_soups
            else:
                actors_soup_tag = actor_soups[0]

            actors = [
                actor.get_text()
                for actor in actors_soup_tag.find_all(
                    "a", attrs={"class": re.compile("styles_link")}
                )
            ]

            if voice_actors_tag is not None:
                voice_actors = [
                    actor.get_text()
                    for actor in voice_actors_tag.find_all(
                        "a", attrs={"class": re.compile("styles_link")}
                    )
                ]

        return Cast(actors, voice_actors)

    def get_rating(self) -> UserRating:
        rating_count_imdb = self.NA_TAG
        rating_count_kinopoisk = self.NA_TAG

        rating_kinopoisk = self.show_soup.find_all(
            "a", attrs={"class": re.compile("film-rating-value")}
        )
        rating_imdb = self.show_soup.find_all(
            "span", attrs={"class": re.compile("styles_valueSection")}
        )

        if rating_kinopoisk:
            rating_kinopoisk = rating_kinopoisk[0].get_text()

            rating_count_kinopoisk = self.show_soup.find_all(
                "span", attrs={"class": re.compile("styles_count")}
            )[0].get_text()
        else:
            rating_kinopoisk = self.NA_TAG

        if rating_imdb:
            rating_imdb = rating_imdb[0].get_text()

            rating_count_imdb = (
                self.show_soup.find_all(
                    "div", attrs={"class": re.compile("film-sub-rating")}
                )[0]
                .find("span", attrs={"class": re.compile("styles_count")})
                .get_text()
            )
        else:
            rating_imdb = self.NA_TAG

        return UserRating(
            rating_kinopoisk, rating_count_kinopoisk, rating_imdb, rating_count_imdb
        )

    def get_synopsis(self) -> Synopsis:
        synopsis = self.NA_TAG
        synopsis_list = self.show_soup.find_all(
            "div", attrs={"class": re.compile("styles_filmSynopsis")}
        )
        if synopsis_list:
            synopsis = synopsis_list[0].get_text()

        return Synopsis(synopsis)

    def get_critics_rating(self) -> CriticsRating:
        russian_critics_percentage = self.NA_TAG
        russian_critics_number_of_reviews = self.NA_TAG
        world_critics_percentage = self.NA_TAG
        world_critics_star_value = self.NA_TAG
        world_critics_number_of_reviews = self.NA_TAG

        critics = self.show_soup.find_all(
            "div", attrs={"class": re.compile("styles_ratingBar")}
        )

        if critics:
            world_critics = critics[0]
            if "в мире" in world_critics.get_text():
                world_critics_percentage = world_critics.find_all(
                    "span", attrs={"class": re.compile("film-rating-value")}
                )[0].get_text()
                world_critics_star_value = world_critics.find_all(
                    "span", attrs={"class": re.compile("styles_starValue")}
                )[0].get_text()

                world_critics_number_of_reviews_raw = world_critics.find_all(
                    "span", attrs={"class": re.compile("styles_count")}
                )[0].get_text()

                world_critics_number_of_reviews = self.right_strip_trailing(
                    world_critics_number_of_reviews_raw, world_critics_star_value
                )

            if len(critics) >= 3:
                russian_critics = critics[2]

                russian_critics_percentage = russian_critics.find_all(
                    "span", attrs={"class": re.compile("film-rating-value")}
                )[0].get_text()

                russian_critics_number_of_reviews = russian_critics.find_all(
                    "span", attrs={"class": re.compile("styles_count")}
                )[0].get_text()

        return CriticsRating(
            world_critics_percentage,
            world_critics_star_value,
            world_critics_number_of_reviews,
            russian_critics_percentage,
            russian_critics_number_of_reviews,
        )

    def get_show_info(self) -> dict:
        show_info = asdict(
            ShowPage(
                id=self.get_id(),
                titles=self.get_titles(),
                cast=self.get_actors(),
                info=self.get_info(),
                user_rating=self.get_rating(),
                synopsis=self.get_synopsis(),
                critics_rating=self.get_critics_rating(),
            )
        )

        flatten_dict = {}
        for key, value in show_info.items():
            flatten_dict = {**flatten_dict, **value}

        return flatten_dict
