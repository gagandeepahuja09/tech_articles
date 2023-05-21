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

**Underfitting And Overfitting**

**Experimenting with Different Models**
* Each decision tree node has 2 children.
* Depth = no. of decisions required to come to a decision. If depth = 10, there are 2^10 groups of houses possible.
* *Overfitting*: Large no. of leaves => fewer houses in each leave => unreliable predictions => becasue each prediction is based on only a few houses. 
* *Underfitting*: If no. of leaves is less => each leave will have many houses => which will not be able to capture many patterns and distinctions.
* We need to find the sweet spot for minimal mean absolute error.

**Example**
* We can specify the parameter max_leaf_nodes during defining DecisionTreeRegressor to control the tree depth.
```
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_absolute_error

def get_mae(max_leaf_nodes, train_X, val_X, train_y, val_y):
    model = DecisionTreeRegressor(max_leaf_nodes=max_leaf_nodes, random_state=0)
    model.fit(train_X, train_y)
    preds_val = model.predict(val_X)
    mae = mean_absolute_error(val_y, preds_val)
    return(mae)
```

**Random Forests**
* Can try to solve the overfitting and underfitting problem.
* Random forest uses many trees. It make a prediction by averaging the prediction of each component tree.
* Works well with default params.
* There could be models with even better performance but many of them are sensitive to getting the right parameters.

```
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

forest_model = RandomForestRegressor(random_state=1)
forest_model.fit(train_X, train_y)
preds = forest_model.predict(val_X)
print(mean_absolute_error(val_y, preds))
```
* One of the the best features of random forests is that they work reasonably well even without tuning.