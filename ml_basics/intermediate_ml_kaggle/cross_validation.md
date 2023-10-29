* Cross-validation for better measures of model performance.
* ML is an iterative process.
* We took a data-driven approach for selecting the features as well as model to use.
* There are still some drawbacks to this approach. Our model might have done well on a set of 1000 rows, but it might be inaccurate on another set of 1000 rows.
* Larger validation set: less randomness or noise in our ML model.
    * We can't do that at the expense of removing rows from training set.

* **Cross Validation**: 
    * Let's say we divide the data into 5 folds: f1, f2, ..., f5.
    * fi ==> test, rest validation for each i.
* *Tradeoff*: Preferred for *small datasets*. Not preferred for large datasets as it will take a lot of time to run.
* No specific threshold for deciding, but if our model takes only a few minutes, we can definitely try cross-validation.

`
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.pipeline import Pipeline
    from sklearn.impute import SimpleImputer

    my_pipeline = Pipeline(steps=[('preprocessor', SimpleImputer()),
                                ('model', RandomForestRegressor(n_estimators=50, random_state=0)) ])
`

* The no. of folds are specified via the `cv` parameter.
* *Why MAE is negative here?*: Scikit has a convention that all metrics are defined such that a higher number is better.

`
    from sklearn.model_selection import cross_val_score

    scores = -1 * cross_val_score(my_pipeline, X, y, cv=5, scoring='neg_mean_absolute_error')
`

**Cross-validation exercise, finding appropriate value of n_estimators (no. of decision trees to be included)**

`
    def get_score(n_estimators):
        """Return the average MAE over 3 CV folds of random forest model.
        
        Keyword argument:
        n_estimators -- the number of trees in the forest
        """
        my_pipeline = Pipeline(steps=[
            ('preprocessor', SimpleImputer()),
            ('model', RandomForestRegressor(n_estimators, random_state=0))
        ])
        return (-1 * cross_val_score(my_pipeline, X, y,
                                cv=3,
                                scoring='neg_mean_absolute_error')).mean()
`

* Finding the value of n_estimators which will give the lower MAE and plotting that in a graph.

`
    import matplotlib.pyplot as plt
    %matplotlib inline

    results = { i : get_score(i) for i in range(50, 401, 50) }    
    plt.plot(list(results.keys()), list(results.values()))
    plt.show()
`