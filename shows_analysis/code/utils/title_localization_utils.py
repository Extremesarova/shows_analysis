import re
from typing import List, Tuple

import numpy as np
import pandas as pd
import torch
from sentence_transformers import util
from torch import Tensor


def check_countries(country, filters):
    for filter_ in filters:
        if filter_ in country:
            return False
    return True


def has_numbers_in_square_brackets(s):
    return bool(re.search(r"\(.*\)", s))


def get_embeddings(model, texts: List[str]) -> Tensor:
    texts_lowercase = list(map(str.lower, texts))
    with torch.no_grad():
        text_embeddings = model.encode(texts_lowercase, convert_to_tensor=True)
    return text_embeddings


def compute_embeddings(
    model, russian_titles: np.array, original_titles: np.array
) -> Tuple[Tensor]:
    russian_title_embs = get_embeddings(model, russian_titles)
    original_title_embs = get_embeddings(model, original_titles)

    return russian_title_embs, original_title_embs


def compute_similarity(
    russian_title_embs: Tensor, original_title_embs: Tensor
) -> Tensor:
    return util.cos_sim(russian_title_embs, original_title_embs).cpu().detach().numpy()


def get_similarity_dataframe(
    model, russian_titles, original_titles, sort=False, ascending=True
):
    embeddings = compute_embeddings(model, russian_titles, original_titles)
    similarity_scores = compute_similarity(*embeddings)

    rows = []
    for i in range(len(russian_titles)):
        rows.append([russian_titles[i], original_titles[i], similarity_scores[i][i]])

    similarity_df = pd.DataFrame(
        data=rows, columns=["russian_title", "original_title", "similarity"]
    )
    similarity_df["similarity"] = similarity_df["similarity"].apply(
        lambda similarity: round(similarity, 3)
    )

    del embeddings
    torch.cuda.empty_cache()

    similarity_df = (
        similarity_df.sort_values(by="similarity", ascending=ascending)
        if sort
        else similarity_df
    )

    return similarity_df
