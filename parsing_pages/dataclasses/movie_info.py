from dataclasses import dataclass
from typing import List


@dataclass
class MovieId:
    id: int


@dataclass
class MovieTitles:
    russian_title: str
    original_title: str


@dataclass
class MovieCast:
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
    marketing: str
    us_box_office: str
    world_box_office: str
    viewers: List[str]
    russian_premiere: str
    world_premiere: str
    dvd_release: str
    blue_ray_release: str
    age_rating: str
    mpaa_rating: str
    duration: str

    # @classmethod
    # def from_dict_to_dataclass(cls, data):
    #     return cls(
    #         **{
    #             key: (data[key] if val.default == val.empty else data.get(key, val.default))
    #             for key, val in inspect.signature(MovieInfo).parameters.items()
    #         }
    #     )


@dataclass
class Movie:
    id: MovieId
    titles: MovieTitles
    cast: MovieCast
    info: MovieInfo
