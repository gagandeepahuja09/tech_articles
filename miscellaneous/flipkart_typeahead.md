**Hyper-personalized Type-ahead Search At Flipkart**

* If your past history suggests that you have bought a lot of shoes, then it should come at the top when typing sh.
* Minimize the time taken to purchase for a user.

**Parameters for Ranking**

1. Quality of the suggestion
    - Popularity: How popular the term is? Even if it is hyper personalized, it should not be shown if it is not popular upto a threshold.
    - Enough no. of results: If it doesn't have enough no. of results, then showing it would be a poor user experience.
    - Grammar quality

2. Prefix: We could have logic only based on prefix or on substring or some other or consider fuzzy scenarios, typos, etc.

3. User dependent (past action):
    - Historical purchases might have higher weightage than historical searches.
    - We might prioritize recent searches.