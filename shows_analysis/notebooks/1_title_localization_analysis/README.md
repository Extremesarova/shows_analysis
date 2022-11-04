# Research on the quality of localization of movie titles

[Notebook](https://nbviewer.org/github/Extremesarova/shows_analysis/blob/main/shows_analysis/notebooks/1_title_localization_analysis/movie_title_translation.ipynb)

The goal of this research was to find out:

1) How similar Russian titles and original titles are in general?
2) Can we split dissimilar pairs (`Russian title` :: `original title`) into groups by root cause?

**Results**:

In general, I can say that the titles are somewhat similar - the title similarity distribution is left-skewed.  
<img src="../../../static/title_similarity.png" width="482" height="240"/>

Average similarity is equal to 0.73 (median is 0.78)

There are a few cases for dissimilarity:  
1) **Russian title is a cropped version of original title**  
    <span style="color:grey">Another problem in this case can be the fact that embeddings don't work very well with proper names like Borat :: Борат, Dolittle :: Дулиттл, and so on.</span>

    Examples:

    * Борат (Borat) :: Borat: Cultural Learnings of America for Make Benefit Glorious Nation of Kazakhstan
    * Веном 2 (Venom 2) :: Venom: Let There Be Carnage
    * Бёрдмэн (Birdman) :: Birdman or (The Unexpected Virtue of Ignorance)
    * Амели (Amelie) :: Le Fabuleux destin d'Amélie Poulain

2) **Russian title is an extended version of original title**  
    <span style="color:grey">Remark about proper names applies to this case too.</span>  
    Examples:

    * Удивительное путешествие доктора Дулиттла (The Amazing Journey of Doctor Dolittle) :: Dolittle
    * Пол: Секретный материальчик (Paul: Secret material) :: Paul
    * Рапунцель: Запутанная история (Rapunzel: Tangled) :: Tangled

3) **Russian title was localized (made up) by translators/localizers**  
    <span style="color:grey">Sometimes it is better to localize the title due to cultural and other peculiarities, but sometimes it goes too far.</span>
    Examples:

    * Невероятный мир глазами Энцо :: The Art of Racing in the Rain
    * Человек, который изменил всё (The man who changed everything) :: Moneyball
    * Области тьмы (Areas of darkness) :: Limitless
    * Одинокий волк (Lone wolf) :: Clean
