import re

from bs4 import BeautifulSoup, Tag

from parsing_pages.dataclasses.movie_info import MovieId, Review, Reviews
from parsing_pages.preprocessing.preprocessor import Preprocessor


class MovieReviewsParser:
    KINOPOISK_URL = "https://www.kinopoisk.ru"
    MOVIE_URL_TEMP = f"{KINOPOISK_URL}/film/"

    def __init__(self, reviews_soup):
        self.reviews_soup = reviews_soup
        self.preprocessor = Preprocessor()
        self.movie_id = self.get_id().id
        self.movie_reviews = self.get_reviews()

    def return_score(self, review: str) -> str:
        scores = []
        score = "N/A"
        for s in review.split("<p>")[-3:]:
            if self.preprocessor.has_numbers(s) and (("/" in s) or ("из" in s)):
                scores.append(s)

        score_candidate = BeautifulSoup(scores[-1]).get_text() if scores else "N/A"
        if scores and len(score_candidate.split(" ")) <= 4 and score_candidate != "N/A":
            score = score_candidate
        return score

    def get_id(self) -> MovieId:
        id = self.reviews_soup.find_all("link", attrs={"href": re.compile(self.MOVIE_URL_TEMP)})[0]
        id = int(id["href"].split("/")[-3])
        return MovieId(id=id)

    def parse_review(self, review: Tag) -> Review:
        username = review.find_all("p", attrs={"class": "profile_name"})[0].get_text()

        movie_id = self.movie_id

        review_id = review.find_all("p", attrs={"class": "profile_name"})[0].find_all("a", href=True)[0]
        review_id = int(review_id["href"].split("/")[-2])

        datetime = review.find_all("span", attrs={"class": "date"})[0]
        datetime = datetime.get_text().replace("|", "").strip()
        datetime = " ".join(datetime.split())

        sentiment = review.find("div", attrs={"class": "response"}).attrs["class"][-1]

        subtitle = review.find("p", attrs={"class": "sub_title"}).get_text()

        review_body = review.find("span", attrs={"itemprop": "reviewBody"}).contents
        review_body_score = "<p>".join(
            [
                str(el).replace("\n", "")
                for el in review_body
                if str(el) not in ["<br/>", "\n"]
            ]
        )

        score = self.return_score(review_body_score)

        review_body = review.find_all("span", attrs={"itemprop": "reviewBody"})[0].get_text()
        review_body = "<p>".join([str(el) for el in review_body.split("\n\n")])

        usefulness_ratio = review.find("li", attrs={"id": re.compile("comment_num_vote")}).get_text()

        direct_link = review.find("p", attrs={"class": "links"}).find(href=True)
        direct_link = self.KINOPOISK_URL + direct_link["href"] if direct_link else "N/A"

        return Review(movie_id, review_id, username, datetime, sentiment, subtitle, review_body, score,
                      usefulness_ratio, direct_link)

    def get_reviews(self) -> Reviews:
        reviews = self.reviews_soup.find_all("div", attrs={"class": "reviewItem userReview"})
        review_list = []
        for review in reviews:
            review_list.append(self.parse_review(review))

        return Reviews(review_list)
