import re
from typing import List

import dateparser
from bs4 import BeautifulSoup
from tqdm.auto import tqdm


def normalize_datetime(datetime: str) -> str:
    return dateparser.parse(datetime).strftime("%d.%m.%Y %H:%M")


def return_score(preprocessor, review: str) -> str:
    scores = []
    score = ""
    splitted_review = review.split("<p>")

    # looking only at the last three sentences
    for s in splitted_review[-3:]:
        if preprocessor.has_numbers(s) and (("/" in s) or ("из" in s)):
            scores.append(s)

    # taking only the last match
    score_candidate = (
        BeautifulSoup(scores[-1], "html.parser").get_text() if scores else ""
    )

    # sum of digits in the string - useful, if digits are big
    sum_scores = sum([int(number) for number in re.findall(r"\d+", score_candidate)])

    if (
        scores
        and len(score_candidate.split(" ")) <= 4
        and score_candidate != ""
        and sum_scores < 50
    ):
        score = score_candidate

    score_index = (
        splitted_review.index(scores[-1])
        if scores and scores[-1] in splitted_review
        else None
    )

    return score.strip(), score_index


def clean_reviews_from_scores(reviews: List[str], score_sentence_indices: List[int]):
    assert len(score_sentence_indices) == len(reviews)
    cleaned_reviews = []

    for review, score_sentence_index in tqdm(
        zip(reviews, score_sentence_indices),
        total=len(reviews),
        desc="Removing scores from reviews",
    ):
        splitted_review = review.split("<p>")
        if isinstance(score_sentence_index, str):
            print(score_sentence_index)
        if score_sentence_index is not None:
            del splitted_review[score_sentence_index]

        cleaned_reviews.append("<p>".join(splitted_review))

    return cleaned_reviews


def cast_score_to_float(
    score_string: str,
    regex_expression: str = "[-+]?[.]?[\d]+(?:,\d\d\d)*[\.]?\d*(?:[eE][-+]?\d+)?",
) -> float:
    real_numbers = re.findall(regex_expression, score_string)
    real_numbers = [float(number) for number in real_numbers]

    score = real_numbers[0] if len(real_numbers) >= 1 else None

    if score is not None:
        score = 10.0 if score > 10.0 else score
        score = 0.0 if score < 0.0 else score

    return score
