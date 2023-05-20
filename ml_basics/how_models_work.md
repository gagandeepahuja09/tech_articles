* https://www.kaggle.com/learn
* Identify past patterns and make decisions.
* Decision trees: simpler and basic building block for some of the best models in data science.
    * It is like if-else only?
    * Final decision: at the leafs.

**Basic Data Exploration**
* `import pandas as pd`
* DataFrame data structure helps with performing various operations on table, filtering, data-visualization.
* We can use the describe method to get details like: count, min, max, std deviation, 25 percentile, 50p, 75p for each field.
    * count ==> count of non-missing values.
    * std deviation ==> how numerically spread out the values are.
* Exercise
    * Step 1: specify file path and read using pandas read csv function.
    * Step 2: review the data.
    * Think about your data.
        * Is this accurate? What could be the limitations?
    * data = pd.read_csv
    * data.describe
    * data.columns

**Selecting Data For Modeling**
* Picking few variables using intuition.
* There are stastical techniques to automatically prioritize variables.
* data.Columns
* Handling missing values.
    * dropping missing values.
    * data = data.dropna(axis=0)

**Dot Notation To Predict Select Columns: Prediction Target(y)**
* This is more like a series.
* y = data.Price

**Features (Input Columns For Models) (X)**
* Eg: We are building a model to determine the price of a house. all the columns that will help in predicting that would be the features.