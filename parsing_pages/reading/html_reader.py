from bs4 import BeautifulSoup


class PageReader:
    """Reading web-page into BeautifulSoup object"""

    def __init__(self, path: str):
        self.path = path

    def _read_page(self) -> str:
        with open(self.path, "r", encoding='utf-8') as f:
            page = f.read()

        return page

    def get_soup(self) -> BeautifulSoup:
        page = self._read_page()
        soup = BeautifulSoup(page, "html.parser")

        return soup
