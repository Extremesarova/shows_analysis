from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from IPython.display import set_matplotlib_formats

set_matplotlib_formats("retina")


def plot_per_type(
    dataframe: pd.DataFrame,
    column: str,
    title: str,
    title_shift: int = 1.1,
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

    f.suptitle(title, y=title_shift)
    plt.show()


def plot_dt_per_type(
    dataframe: pd.DataFrame,
    column: str,
    title: str,
    title_shift: int = 1.0,
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

    f.suptitle(title, y=title_shift)

    plt.show()


def plot_catplot(
    y: str,
    x: str,
    hue: str,
    data: pd.DataFrame,
    title: str,
    kind: str = "box",
    order: List[str] = ["negative", "neutral", "positive"],
    medianprops: dict = {"color": "red", "lw": 1},
):
    if kind == "box":
        plot = sns.catplot(
            y=y,
            x=x,
            hue=hue,
            data=data,
            kind=kind,
            order=order,
            medianprops=medianprops,
        )
    else:
        plot = sns.catplot(y=y, x=x, hue=hue, data=data, kind=kind, order=order)

    plot.figure.subplots_adjust(top=0.9)
    plot.fig.suptitle(title)
    plt.show()
