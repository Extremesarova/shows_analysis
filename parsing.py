import multiprocessing
import os
from pathlib import Path
from typing import Tuple

import pandas as pd
from loguru import logger
from tqdm.contrib.concurrent import process_map  # or thread_map

from config.config_reader import ConfigReader
from parsing_pages.parsers.movie_info_parser import MovieInfoParser
from parsing_pages.parsers.movie_reviews_parser import MovieReviewsParser
from parsing_pages.reading.html_reader import PageReader
from utils import get_page_type


def run_multiprocessing(func, i, n_processors):
    # with Pool(processes=n_processors) as pool:
    #     return pool.map(func, i)
    return process_map(func, i, max_workers=n_processors, chunksize=1)


def get_review_dict(path: str) -> dict:
    soup = PageReader(path).get_soup()
    movie_review_parser = MovieReviewsParser(soup)

    return movie_review_parser.movie_reviews


def get_movie_dict(path: str) -> dict:
    soup = PageReader(path).get_soup()
    movie_info_parser = MovieInfoParser(soup)
    movie_dict = movie_info_parser.movie_info

    return movie_dict


def get_movie_and_review_dict(path: str) -> Tuple[dict, str]:
    str_path = str(path)
    page_type = get_page_type(str_path)

    if page_type == "review":
        review_dict = get_review_dict(str_path)
        return review_dict, page_type
    else:
        movie_dict = get_movie_dict(str_path)
        return movie_dict, page_type


def main():
    config = ConfigReader().config
    data_path = config.get("path", "path_to_data")
    save_path = config.get("path", "path_to_save")
    n_processors = multiprocessing.cpu_count()
    logger.info(f"The number of processors is {n_processors}")

    movie_rows_list = []
    review_rows_list = []

    pathlist = list(Path(data_path).rglob("*.html"))

    results = run_multiprocessing(get_movie_and_review_dict, pathlist, n_processors)

    for info_dict, page_type in results:
        if page_type == "front":
            movie_rows_list.append(info_dict)
        else:
            review_rows_list.extend(info_dict)

    movie_df = pd.DataFrame(movie_rows_list)
    movie_df.to_parquet(os.path.join(save_path, "movies.parquet"), index=False)

    review_df = pd.DataFrame(review_rows_list)
    review_df.to_parquet(os.path.join(save_path, "reviews.parquet"), index=False)


if __name__ == "__main__":
    main()
