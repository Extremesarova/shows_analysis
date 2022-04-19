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

    pathlist = Path(data_path).rglob("*.html")
    for path in tqdm(pathlist):
        str_path = str(path)
        page_type = get_page_type(str_path)

        if page_type == "review":
            continue
            soup = PageReader(str_path).get_soup()
            movie_review_parser = MovieReviewsParser()
        else:
            # print(str_path, page_type)
            soup = PageReader(str_path).get_soup()
            movie_info_parser = MovieInfoParser(soup)
            movie_dict = asdict(movie_info_parser.movie_info)
            flatten_dict = {}
            for key, value in movie_dict.items():
                flatten_dict = {**flatten_dict, **value}
            movie_rows_list.append(flatten_dict)

    movie_df = pd.DataFrame(movie_rows_list)
    movie_df.to_csv("movie_info.csv", index=False)


if __name__ == "__main__":
    main()
