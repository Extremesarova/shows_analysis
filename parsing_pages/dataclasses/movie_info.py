import inspect
from dataclasses import dataclass
from typing import List


@dataclass
class ShowId:
    id: int


@dataclass
class Titles:
    russian_title: str
    original_title: str


@dataclass
class Cast:
    actors: List[str]
    voice_actors: List[str]


@dataclass
class MovieInfo:
    year: int
    country: List[str]
    genre: List[str]
    slogan: str
    director: List[str]
    scriptwriter: List[str]
    producer: List[str]
    operator: List[str]
    composer: List[str]
    artist: List[str]
    cut: List[str]
    budget: str
    us_box_office: str
    world_box_office: str
    viewers: List[str]
    russian_box_office: str
    russian_premiere: str
    world_premiere: str
    dvd_release: str
    blue_ray_release: str
    age_rating: str
    mpaa_rating: str
    duration: str
    digital_release: str
    marketing: str
    platform: str
    rerelease: str
    film_director: str


def from_dict_to_dataclass(cls, data):
    return cls(
        **{
            key: data[key] if key in data else ""
            for key, val in inspect.signature(MovieInfo).parameters.items()
        }
    )


@dataclass
class UserRating:
    rating_kinopoisk: str
    rating_count_kinopoisk: str
    rating_imdb: str
    rating_count_imdb: str


@dataclass
class Synopsis:
    synopsis: str


@dataclass
class CriticsRating:
    world_critics_percentage: str
    world_critics_star_value: str
    world_critics_number_of_reviews: str
    russian_critics_percentage: str
    russian_critics_number_of_reviews: str


@dataclass
class MoviePage:
    id: ShowId
    titles: Titles
    cast: Cast
    info: MovieInfo
    user_rating: UserRating
    synopsis: Synopsis
    critics_rating: CriticsRating
