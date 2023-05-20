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
```
    melbourne_features = ['Rooms', 'Bathroom', 'Landsize', 'Latitude', 'Longitude']
    X = melbourne_data[melebourne_features]
    X.describe()
    X.head() // top few rows
```

**Building A Model**
* scikit-learn ==> ML library in Python.
* *Define*: 
    * What type of model will it be? (eg. Decision tree)
    * We can also specify parameters specific to the model type.

```
from sklearn.tree import DecisionTreeRegressor
# Ensure same results each run
model = DecisionTreeRegressor(random_state=1)
```

* *Fit: Heart of modelling*
    * Capture patterns from provided data.
    * ```model.fit(X, y)```
        * X ==> features
        * y ==> Prediction target (price)
* *Predict*
    * Will predict the price of 5 houses.
    * ```model.predict(X.head())```
* *Evaluate*

**Model Validation**
* *Predictive accuracy*
* We'll find a mix of good and bad predictions. Looking through the entire list is sort of pointless.
* We need to summarize in a single metric.
* *Mean Absolute Error*
```
    from sklearn.metrics import mean_absolute_error
    predicted_prices = model.predict(X)
    mean_absolute_error(y, predicted_prices)
```

**Validation Data**: We exclude some data from model-building process. We then use that data to test the model's accuracy on data it hasn't seen before.

**Coding It**
```
    from sklearn.model_selection import train_test_split

    train_X, val_X, train_y, val_y = train_test_split(X, y, random_state = 0)
    model = DecisionTreeRegressor()
    model.fit(train_X, train_y)

    val_predictions = model.predict(val_X)
    print(mean_absolute_error(val_y, val_predictions)) 
```