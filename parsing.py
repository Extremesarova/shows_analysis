import os
from functools import partial
from pathlib import Path
from typing import Tuple

import pandas as pd
import typer
from loguru import logger
from tqdm.contrib.concurrent import process_map

from parsing_pages.parsers.movie_info_parser import MovieInfoParser
from parsing_pages.parsers.reviews_parser import ReviewsParser
from parsing_pages.parsers.series_info_parser import SeriesInfoParser
from parsing_pages.reading.html_reader import PageReader
from utils import get_page_type

app = typer.Typer()


def run_multiprocessing(func, i, n_processors):
    # with Pool(processes=n_processors) as pool:
    #     return pool.map(func, i)
    return process_map(func, i, max_workers=n_processors, chunksize=1)


def get_review_dict(path: str) -> dict:
    soup = PageReader(path).get_soup()
    reviews_parser = ReviewsParser(soup)

    return reviews_parser.reviews


def get_show_dict(show_parser, path: str) -> dict:
    soup = PageReader(path).get_soup()

    return show_parser(soup).show_info


def get_show_and_review_dicts(show_parser, path: str) -> Tuple[dict, str]:
    str_path = str(path)
    page_type = get_page_type(str_path)

    if page_type == "review":
        review_dict = get_review_dict(str_path)
        return review_dict, page_type
    else:
        show_dict = get_show_dict(show_parser, str_path)
        return show_dict, page_type


def save_dfs(data_path: str, show_type: str, show_rows: list, review_rows: list):
    movie_df = pd.DataFrame(show_rows)
    movie_df.to_parquet(os.path.join(data_path, f"{show_type}_info.parquet"), index=False)

    review_df = pd.DataFrame(review_rows)
    review_df.to_parquet(os.path.join(data_path, f"{show_type}_reviews.parquet"), index=False)


def parse_pages(show_type: str, read_path: str, n_processors: int):
    pathlist = list(Path(read_path).rglob("*.html"))

    logger.info(f"The number of processors for multiprocessing is {n_processors}")

    show_rows = []
    review_rows = []
    show_parser = MovieInfoParser if show_type == "movies" else SeriesInfoParser

    parse_shows = partial(get_show_and_review_dicts, show_parser)

    results = run_multiprocessing(parse_shows, pathlist, n_processors)

    for info_dict, page_type in results:
        if page_type == "front":
            show_rows.append(info_dict)
        else:
            review_rows.extend(info_dict)

    return show_rows, review_rows


@app.command()
def parse(data_path: str, show_type: str, n_processors: int):
    read_path = os.path.join(data_path, show_type)
    show_rows, review_rows = parse_pages(show_type, read_path, n_processors)
    save_dfs(data_path, show_type, show_rows, review_rows)


if __name__ == "__main__":
    app()
