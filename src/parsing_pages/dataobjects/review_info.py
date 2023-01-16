from dataclasses import dataclass
from typing import List


@dataclass
class Review:
    show_id: int
    username: str
    datetime: str
    sentiment: str
    subtitle: str
    review_body: str
    usefulness_ratio: str
    direct_link: str


@dataclass
class Reviews:
    review: List[Review]
