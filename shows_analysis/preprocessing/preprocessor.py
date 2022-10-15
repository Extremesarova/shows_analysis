import re

import unicodedata


class Preprocessor:
    CLEANER_MAP = {"\t": "", "\n": "", "\r": ""}

    def __init__(self):
        self.translator: dict = str.maketrans(self.CLEANER_MAP)

    def preprocess_string(self, str_: str) -> str:
        str_ = unicodedata.normalize("NFKD", str_)
        str_ = str_.translate(self.translator)
        str_ = " ".join(str_.split())

        return str_

    @staticmethod
    def has_numbers(str_: str) -> bool:
        return bool(re.search(r"\d", str_))
