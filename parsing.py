import os
from dataclasses import asdict
from pathlib import Path

import pandas as pd
from tqdm import tqdm

from config.config_reader import ConfigReader
from parsing_pages.parsers.movie_info_parser import MovieInfoParser
from parsing_pages.parsers.movie_reviews_parser import MovieReviewsParser
from parsing_pages.reading.html_reader import PageReader
from utils import get_page_type


def main():
    config = ConfigReader().config
    data_path = config.get("path", "data")

    movie_rows_list = []
    review_rows_list = []

    _, _, files = next(os.walk(data_path))
    file_count = len(files)

    pathlist = Path(data_path).rglob("*.html")
    for path in tqdm(pathlist, total=file_count, desc="Parsing movie pages", unit="page"):
        str_path = str(path)
        page_type = get_page_type(str_path)

        if page_type == "review":
            soup = PageReader(str_path).get_soup()
            movie_review_parser = MovieReviewsParser(soup)
            review_dict = asdict(movie_review_parser.movie_reviews)['review']
            review_rows_list.extend(review_dict)
        else:
            soup = PageReader(str_path).get_soup()
            movie_info_parser = MovieInfoParser(soup)
            movie_dict = asdict(movie_info_parser.movie_info)
            flatten_dict = {}
            for key, value in movie_dict.items():
                flatten_dict = {**flatten_dict, **value}
            movie_rows_list.append(flatten_dict)

    movie_df = pd.DataFrame(movie_rows_list)
    movie_df.to_csv("movies.csv", index=False)

    review_df = pd.DataFrame(review_rows_list)
    review_df.to_csv("reviews.csv", index=False)


if __name__ == "__main__":
    main()
