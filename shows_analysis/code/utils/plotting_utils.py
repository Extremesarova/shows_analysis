from typing import Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from IPython.display import set_matplotlib_formats

set_matplotlib_formats("retina")


def plot_per_type(
    dataframe: pd.DataFrame,
    column: str,
    title: str,
    bins: int = 10,
    figsize: Tuple[int] = (8, 4),
):
    f, ax = plt.subplots(1, 2, figsize=figsize)

    dataframe[dataframe["type"] == "movie"][column].plot.hist(
        ax=ax[0], edgecolor="black", color="red", bins=bins
    )
    ax[0].set_title("Type = movie")

    dataframe[dataframe["type"] == "series"][column].plot.hist(
        ax=ax[1], edgecolor="black", color="green", bins=bins
    )
    ax[1].set_title("Type = series")

    f.tight_layout()
    f.suptitle(title, y=1.1)
    plt.show()


def plot_dt_per_type(
    dataframe: pd.DataFrame,
    column: str,
    title: str,
    bins: int = 24,
    figsize: Tuple[int] = (14, 4),
):
    f, ax = plt.subplots(1, 2, figsize=figsize)

    dataframe[dataframe["type"] == "movie"][column].hist(
        ax=ax[0], edgecolor="black", color="red", bins=np.arange(bins + 1) - 0.5
    )
    ax[0].set_title("Type = movie")
    ax[0].set_xticks(range(bins), minor=False)
    ax[0].grid(visible=None)

    dataframe[dataframe["type"] == "series"][column].hist(
        ax=ax[1], edgecolor="black", color="green", bins=np.arange(bins + 1) - 0.5
    )
    ax[1].set_title("Type = series")
    ax[1].set_xticks(range(bins), minor=False)
    ax[1].grid(visible=None)

    f.suptitle(title, y=1.0)

    plt.show()
