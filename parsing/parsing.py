from pathlib import Path

from config.config_reader import ConfigReader
from parsing.parsers.movie_info_parser import MovieInfoParser
from parsing.parsers.movie_reviews_parser import MovieReviewsParser
from parsing.reading.html_reader import PageReader
from utils import get_page_type


def main():
    config = ConfigReader().config
    data_path = config["path"].get("data")

    pathlist = Path(data_path).rglob("*.html")
    for path in pathlist:
        str_path = str(path)
        page_type = get_page_type(str_path)
        soup = PageReader(str_path).soup

        if page_type == "review":
            movie_review_parser = MovieReviewsParser()
        else:
            movie_info_parser = MovieInfoParser(soup)

        print(str_path, page_type)


if __name__ == "__main__":
    main()
