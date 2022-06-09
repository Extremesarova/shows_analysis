from dataclasses import dataclass
from typing import List


@dataclass
class SeriesInfo:
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
    russian_box_office: str
    russian_premiere: str
    world_premiere: str
    dvd_release: str
    blue_ray_release: str
    age_rating: str
    mpaa_rating: str
    duration: str
    digital_release: str
    platform: str
    film_director: str
