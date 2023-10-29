* **Ensemble methods**: 
    * Eg: RandomForest: averaging the prediction of many decision trees.
    * Ensemble methods combine the prediction of several models.

**Gradient**
* Goes through cycles to iteratively add models into an ensemble.
* We start with a single naive model and determine the model parameters, so that adding this new model to the ensemble will reduce the loss. 
* *Steps*
    1. Start with a naive model.
    2. Start the cycle:
        * Make predictions with the current ensemble. The prediction from all models are added to the ensemble.
        * Calculate loss function from the predictions.
        * Determine model parameters, so that adding this new model to the ensemble will reduce the loss.
        * Gradient descent is used on the loss function to determine the parameters in the new model. 

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
    * How many times to go through the modeling cycle. Also equal to the number of models as we will keep adding 1 new model in each cycle.
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

`
    my_model = XGBRegressor(n_estimators=1000, learning_rate=0.05)
    my_model.fit(X_train, y_train, early_stopping_rounds=5, eval_set=[ (X_valid, y_valid) ], verbose=False)
`

3. *learning_rate*
    * Let's say that the loss function is root mean squared error.
    * Rather than setting `new_prediction = old_prediction - gradient`, we set it as `new_prediction = old_prediction - (learning_rate * gradient)`. Learning rate is typically less than 1. Default value = .1.
    * It means that each model that we use helps us less.
    * It helps with more gradual convergence towards the optimal solution but is computationally more expensive.
    * This helps avoid overfitting.

4. *n_jobs*
    * Using parallelism to build our models faster. 
    * `n_jobs` is typically set to no. of CPU cores in the machine.
    * Useful only in large datasets.