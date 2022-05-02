from dataclasses import dataclass
from typing import List


@dataclass
class Review:
    movie_id: int
    review_id: int
    username: str
    datetime: str
    sentiment: str
    subtitle: str
    review_body: str
    score: str
    usefulness_ratio: str
    direct_link: str


@dataclass
class Reviews:
    review: List[Review]
