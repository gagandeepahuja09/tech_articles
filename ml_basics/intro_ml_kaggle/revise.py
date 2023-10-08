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