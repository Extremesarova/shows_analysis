# Analysis

## [Research on the quality of localization of movie titles](https://nbviewer.org/github/Extremesarova/shows_analysis/blob/main/shows_analysis/notebooks/analysis/1_title_localization_analysis/movie_title_translation.ipynb)  

The goal of this research is to find out:

1) How similar Russian titles and original titles are in general?
2) Can we split dissimilar pairs (Russian title::original title) into groups by root cause?

**Results**:

In general, I can say that the titles are somewhat similar - the title similarity distribution is left-skewed.  
<img src="../../../../static/title_similarity.png" width="482" height="240"/>

Average similarity is equal to 0.73 (median is 0.78)

1) There are a few cases for dissimilarity:  
    **Russian title is a cropped version of original title**  
    <span style="color:grey">Another problem in this case can be the fact that embeddings don't work very well with proper names like Borat::Борат, Dolittle::Дулиттл, and so on.</span>

    Examples:

    * Борат::Borat: Cultural Learnings of America for Make Benefit Glorious Nation of Kazakhstan
    * Веном 2::Venom: Let There Be Carnage
    * Бёрдмэн::Birdman or (The Unexpected Virtue of Ignorance)
    * Амели::Le Fabuleux destin d'Amélie Poulain

    **Russian title is an extended version of original title**  
    <span style="color:grey">Remark about proper names applies to this case too.</span>  
    Examples:
    * Удивительное путешествие доктора Дулиттла::Dolittle
    * Пол: Секретный материальчик::Paul
    * Рапунцель: Запутанная история::Tangled

    **Russian title was localized (made up) by translators/localizers**  
    Sometimes it is better to localize the title due to cultural and other peculiarities, but sometimes it goes too far.  
    Examples:
    * Невероятный мир глазами Энцо::The Art of Racing in the Rain
    * Человек, который изменил всё::Moneyball
    * Области тьмы::Limitless
    * Одинокий волк::Clean
