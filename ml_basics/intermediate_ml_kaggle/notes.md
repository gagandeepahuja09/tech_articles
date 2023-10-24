**Topics**
* Tackle data type often found in real-world problems. (*missing values, categorical variables*).
* Design *pipelines* to improve the quality of ML code.
* Advanced validation: *Cross-validation*.
* *XGBoost*
* *Data-leakage*

* RandomForestRegressor
    * Parameters: n_estimators, random_state, criterion, max_depth

* *Outputting Csv Result*
```
    preds = model.predict(X)
    output = pd.DataFrame({ 'Id': X.index, 'SalePrice': preds})
    output.to_csv('submission.csv', index=False)
```

# 1. Missing Values
* Question: why drop missing values from ML model?
    * Take decision tree example: it will make suboptimal choices for splits.
* Potential cases:
    * A 2 bedroom house won't have a value for the size of the third room.
    * A survey respondent may choose not to share his income.
* Most ML libraries including scikit-learn give an error if we try to build a model using missing values.
* *Three Approaches*
    1. Drop cols with missing values.
        * Looses access to a lot of potentially useful information.
        * Eg: a column has only a single missing entry and we deleted the entire column. 
    2. *Imputation*
        * Fill the missing value with some number. eg: *mean value of the column*.
        * Useful in most cases.
    3. An extension to imputation
        * Actual values may be above or below the mean (which weren't shared).
        * Missing values may be unique in some other way.
        * Our model might make better predictions by considering values which were originally missing.
        * Step1: Impute, Step2: For each column with missing values, we add a new column which signifies in boolean whether the value was missing. (eg: column name: bed_was_missing).

`
    from sklearn.ensemble import RandomForestRegressor


    data = pd.read_csv('../melb_data.csv')
    # Target
    y = data.Price

    # To keep things simple, keep only numerical predictors
    melb_predictors = data.drop(['Price'], axis=1)
    X = melb_predictors.select_dtypes(exclude=['object'])
    X_train, X_valid, y_train, y_valid = train_test_split(X, y, train_size=.8, test_size=.2, random_state = 0)

    def score_dataset(X_train, X_valid, y_train, y_valid):
        model = RandomForestRegressor(n_estimators=10, random_state=0)
        model.fit(X_train, y_train)
        preds = model.predict(X_valid)
        return mean_absolute_error(y_valid, preds)
`

`
    ## Approach 1: Remove missing cols
    # Get names of columns with missing values
    # isnull will give a timeseries of True, False
    # isnull.any will return even if there is a single true ==> which would be when 
    # even one value is missing in a col.
    cols_with_missing = [col for col in X_train.columns
                        if X_train[col].isnull().any()]

    # drop columns with 
    reduced_X_train = X_train.drop(cols_with_missing, axis=1)
    reduced_X_val = X_val.drop(cols_with_missing, axis=1)

    score_dataset(reduced_X_train, reduced_X_val, y_train, y_val)
`

* fit_and_transform ==> first fit and then transform. typically used with 

`
    ## Approach 2: Imputation
    from sklearn.impute import SimpleImputer

    my_imputer = SimpleImputer()
    imputed_X_train = pd.DataFrame(my_imputer.fit_transform(X_train))
    imputed_X_valid = pd.DataFrame(my_impute.transform(X_valid))

    imputed_X_train.columns = X_train.columns
    imputed_X_valid.columns = X_valid.columns

    score_dataset(imputed_X_train, imputed_X_valid, y_train, y_val)
`

**Categorical Variables**
* *Three Approaches*
    1. Drop categorical variables.
    2. Ordinal encoding
        * Only works well if there is a possible ordering of the categories.
            Never(0) < Rarely(1) < Most Days(2) < Every day(3)
    3. One-hot encoding
        * We won't generally use for variables taking more than 15 values.
        * Eg: for color, we can have different columns: Red, Yellow, Green.

**Pipelines**
* Clean up modelling code.
* It bundles the preprocessing and modelling step, so that we can do it as a single step.
* Benefits:
    * *Cleaner code*: We don't manually need to keep track of our training and validation data at each step.
    * *Fewer bugs*: There are fewer opportunies to misapply a step or forget a processing step.
    * *Easier to productionize*
    * *More options for model validation*: Eg: cross-validation. 