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

**Missing Values**
* Potential cases:
    * A 2 bedroom house won't have a value for the size of the third room.
    * A survey respondent may choose not to share his income.
* Most ML libraries including scikit-learn give an error if we try to build a model using missing values.
* *Three Approaches*
    1. Drop cols with missing values.
        * Looses access to a lot of potentially useful information.
    2. Imputation
        * Fill the missing value with some number. eg: *mean value of the column*.
        * Useful in most cases.
    3. An extension to imputation
        * Actual values may be above or below the mean (which weren't shared).
        * Missing values may be unique in some other way.
        * Our model might make better predictions by considering values which were originally missing.
        * Step1: Impute, Step2: For each column with missing values, we add a new column which signifies in boolean whether the value was missing. (eg: column name: bed_was_missing).

**Categorical Variables**
* *Three Approaches*
    1. Drop categorical variables.
    2. Ordinal encoding
        * Only works well if there is a possible ordering of the categories.
            Never(0) < Rarely(1) < Most Days(2) < Every day(3)
    3. One-hot encoding
        * We won't generally use for variables taking more than 15 values.
        * Eg: for color, we can have different columns: Red, Yellow, Green.