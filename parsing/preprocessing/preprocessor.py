import unicodedata


class Preprocessor:
    def __init__(self, cleaner_map: dict = {"\t": "", "\n": "", "\r": ""}):
        self.translator: dict = str.maketrans(cleaner_map)

    def preprocess_string(self, str_: str) -> str:
        str_ = unicodedata.normalize("NFKD", str_)
        str_ = str_.translate(self.translator)
        str_ = " ".join(str_.split())

        return str_
