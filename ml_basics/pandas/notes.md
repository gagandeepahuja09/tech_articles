# 1. Creating, Reading And Writing

`import pandas as pd`

**Creating, Reading And Writing**
* 2 core objects in Pandas: *DataFrame (Table), Series (List)*.
* key-value pair. key => string, value => []anyDataType
`
    pd.DataFrame({
        'Bob': ['I liked it', 'Awful'],
        'Sue': ['It was pretty good' , 'Bland']
    },
    index = ['ProductA', 'ProductB'])
`
* keys act as column labels. what about row labels?
* They are sequential (0, 1, 2, 3, ...) by default.
* *Index*: List of row labels.
`
            Bob             Sue
ProductA    I liked it      It was pretty good
ProductB    Awful           Bland        
`

`
    pd.Series([30, 35, 40], index=['2015 Sales', '2016 Sales', '2017 Sales'], name = 'ProductA')
`
* We can think of a data frame as a bunch of series glued together.


**Reading Data Files**
`
    wine_reviews = pd.read_csv('../input/wine-reviews.csv')
    # use shape to see no of rows, cols
    wine_reviews.shape # output: (129971, 14)
    wine_reviews.heap # first 5 rows
`

# 2. Indexing, Selecting And Assigning
`
    # these native operators are column first, row second.
    reviews = pd.read_csv('../input/wine-reviews.csv')
    reviews.country
    reviews['country'][0]
`

**Index-based selection (iloc)**
* Selecting data based on its numerical position.
    * Selecting the first row:
    `reviews.iloc[0]`
* Both loc, iloc are row first, column second opposite to what we have in native Python.

* To get the first column with iloc.
    `reviews.iloc[:, 0]`
* To get first three value of the first column.
    `reviews.iloc[:3, 0]`
* To get 2nd, 3rd value of the first column.
    `reviews.iloc[1:3, 0]`
* Get some specific values passed in the list.
    `reviews.iloc[[1, 3, 5], 0]`
* We can also specify negative numbers. This [-n:] will give last n entries, counting forwards: [-3:0] ==> (n-2, n-1, n)th rows
    `reviews.iloc[-5:0]`

* **Label-based selection (loc)**
* First value of country column
    `reviews['country'][0]` `reviews.iloc[0, 0]`, `reviews.loc[0, 'country']`
* Getting specific columns that we want using loc.
    `reviews.loc[:, ['taster_name', 'taster_twitter_handle', 'points']]`

* **Indexing choice difference b/w loc and iloc**
* iloc use stdlib indexing scheme ==> [0:10] ==> 0, ..., 9 (last is excluded).
* loc ==> [0:10] ==> 0, ..., 10 (all inclusive)
    * why the difference? loc is for different datatypes, so if we have string, we would want all columns and not excluding something.

**Index Manipulation**

* **Conditional Selection**
