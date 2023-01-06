* People could be searching mainly for 3 things:
    * Food dish: Pizza, Burger
    * Restaurant: Dominos, Pizza Hut
    * Cuisine: Chinese.

* In search engine (Solr), the indexes could be on dish, restaurant.
* While ingesting data to ES, the documents would be the data received from restaurant. It could be details like: Title, desc, menu, ratings and reviews, etc.
* We would also have separate documents for dishes: name, desc, ingredients.
* While searching, we can provide weights to the fields. Eg: title=10, des=1.
* Query: "best coffee near me". This will bring up restaurants having "best" in their name.

* Hence we cannot do lexical match, instead we need: "Natural Language Understanding".
* We need to understand the intent of the query.

* Because of voice search, the queries are more verbose. Eg: 
    * garlic bread with cheese dip and cold drink.

**Understanding Intent**
* Dominos outlet near me
    * Dominos ==> Restaurant
    * Near me ==> Location

**Word2Vec**