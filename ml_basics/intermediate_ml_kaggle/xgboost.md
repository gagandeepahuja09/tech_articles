* **Ensemble methods**: 
    * Eg: RandomForest: averaging the prediction of many decision tree.
    * Ensemble methods combine the prediction of several models.

**Gradient**
* Goes through cycles to iteratively add models into an ensemble.
* We start with a naive model and determine the model parameters, so that adding this new model to the ensemble will reduce the loss. 

`
    from xgboost import XGBRegressor

    my_model = XGBRegressor()
    my_model.fit(X_train, y_train)
`

`
    from sklearn.metrics import mean_absolute_error

    predictions = my_model.predict(X_valid)
    print(mean_absolute_error(predictions, y_valid))
`

**Parameter Tuning**
* For improving the accuracy and training speed.
1. *n-estimators*
    * How many times to go through the modeling cycle.
    * Too-low value: underfitting, Too-high value: overfitting.
    * Typical range: 100-1000, though depends a lot on *learning_rate* parameter.

`
    my_model = XGBRegressor(n_estimators=500)
    my_model.fit(X_train, y_train)
`

2. *early_stopping_rounds*
    * This will stop if the validation score stops improving. With only 1 round it is possible that no improvement is shown by chance, it is better to have slightly high values like 5.
    * When using this, we can set high values of `n-estimators` as we are expecting early stopping rounds to not require that many cycles.
    * When using n-estimators, we need to specify the validation set via `eval_set` field.