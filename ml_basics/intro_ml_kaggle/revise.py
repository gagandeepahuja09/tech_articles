import pandas as pd
from sklearn.tree import DecisionTreeRegressor

melbourne_file_path = '../input/melb_data.csv'
melb_data = pd.read_csv(melbourne_file_path)
melb_data.columns
melb_data = melb_data.drop_na(axis=0)

# Prediction target
y = melb_data.Price

features = ['Rooms', 'Bathroom', 'Landsize', 'Latitude', 'Longitude']
X = melb_data[features]

# **Steps for Building our Model**
# * **Define**: 
#     * What type of model will it be? A decision tree or some other type?
#     * Specify parameters specific to the model.
# * **Fit (training)**:
#     * Capture patterns from provided data.
# * **Predict**
# * **Evaluate** how accurate the model's predictions are.

# Specify a number for random state to ensure same result in each run.
melb_model = DecisionTreeRegressor(random_state=1)
melb_model.fit(X, y)

melb_model.predict(X.head())

# Model validation
# error = actual - predicted
from sklearn.metrics import mean_absolute_error

predicted_home_prices = melb_model.predict(X)
mean_absolute_error(y, predicted_home_prices)

# Problem of "in-sample" scores
# We used a single "sample" for both building the model and evaluating it.
# Patterns should hold when it sees new data, which wasn't really tested.
from sklearn.model_selection import train_test_split
train_X, val_X, train_y, val_y = train_test_split(X, y, random_state = 0)
model = DecisionTreeRegressor(random_state=1)
model.fit(train_X, train_y)

val_predictions = model.predict(val_X)
print(mean_absolute_error(val_y, val_predictions))


# Underfitting and Overfitting
# Tree's depth determines how many splits it had to do before coming to a prediction.
# If we have n splits (depth = n), we have split the tree into 2^n groups.
# If we have too many leaves, we will have very less training data for each leaf.
# This is overfitting and makes very unreliable prediction of new data.
# Captures spurious patterns which won't recur in the future.

# Underfitting ==> when the tree is too shallow, it is not able to capture the 
# distinctions and pattern in the data properly and performs poorly even on training data.
# DecisionTreeRegressor has an argument called max_leaf_nodes which can control 
# underfitting vs overfitting.
from sklearn.metrics import mean_absolute_error 
from sklearn.tree import DecisionTreeRegressor

def get_mae(max_leaf_nodes, train_X, train_y, val_X, val_y):
    model = DecisionTreeRegressor(max_leaf_nodes=max_leaf_nodes, random_state=0)
    model.fit(train_X, train_y)
    preds_val = model.predict(val_X)
    return mean_absolute_error(val_y, preds_val)

for max_leaf_nodes in [5, 50, 500, 5000]:
    print(get_mae(max_leaf_nodes, train_X, train_y, val_X, val_y))


# Random forest tries to solve the problem of overfitting and underfitting. 
# It does so by using many trees and makes a prediction by averaging the prediction 
# of each component tree.
# Better predictive accuracy than a single accuracy and does well with default parameters.
    model = RandomForestRegressor(random_state=0)