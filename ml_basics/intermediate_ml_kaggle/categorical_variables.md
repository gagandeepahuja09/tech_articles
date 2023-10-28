* Two techniques: One-hot and Ordinal encoding.
* Logic for only keeping low cardinality and numerical cols only as features.
`
    import pandas as pd
    from sklearn.model_selection import train_test_split

    # Read the data
    data = pd.read_csv('../melb_data.csv')

    # Separate target from predictors
    y = data.Price
    X = data.drop(['Price'], axis=1)

    # Divide data into training and validation subsets
    X_train_full, X_valid_full, y_train, y_valid = train_test_split(X, y, train_size=0.8, test_size=0.2, random_state=0)

    # Drop columns with missing values (simples approach)
    cols_with_missing = [col for col in X_train_full.columns if X_train_full[col].isnull().any()]
    X_train_full.drop(cols_with_missing, axis=1, inplace=True)
    X_valid_full.drop(cols_with_missing, axis=1, inplace=True)

    # Identify low cardinality columns
    low_cardinality_cols = [col for col in X_train_full.columns if X_train_full[col].dtype == "object" and X_train_full[col].nunique() < 10]

    # Identify numerical columns
    numerical_cols = [col for col in X_train_full.columns if X_train_full[col].dtype in ['int64', 'float64']]

    my_cols = low_cardinality_cols + numeric_cols
    X_train = X_train_full[my_cols].copy()
    X_valid = X_valid_full[my_cols].copy()
`

* Function to measure quality of each approach.
`
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import mean_absolute_error

    def score_dataset(X_train, X_valid, y_train, y_valid):
        model = RandomForestRegressor(n_estimators=100, random_state=0)
        model.fit(X_train, y_train)
        preds = model.predict(X_valid)
        return mean_absolute_error(y_valid, preds)
`

* Approach1: Drop categorical variables
`
    drop_X_train = X_train.select_dtypes(exclude=['object'])
    drop_X_valid = X_valid.select_dtypes(exclude=['object'])
    score_dataset(drop_X_train, drop_X_valid, y_train, y_valid)
`

* Approach2: Ordinal encoding
`
    from sklearn.preprocessing import OrdinalEncoder

    label_X_train = X_train.copy()
    label_X_valid = X_valid.copy()

    ordinal_encoder = OrdinalEncoder()
    label_X_train[low_cardinality_cols] = ordinal_encoder.fit_transform(X_train[object_cols])
    label_X_valid[low_cardinality_cols] = ordinal_encoder.transform(X_valid[object_cols])
`
* We can expect better performance if we provide custom labels.

* *Kaggle exercise Ordinal Encoding case*: It is possible that for categorical variables, validation set has some category which was not there in training set. Such cases will throw an error when trying to do ordinal encoding as certain categories don't have numberic values assigned to them.
    `X_train[col].unique(), X_valid[col].unique()`
* How to solve this problem?
    * Custom ordinal encoder which can deal with new categories.
    * Drop the problematic columns
* Identifying the problematic columns:
`
    objects_cols = [col for col in X_train.columns if X_train[col].dtype == "object"]
    good_label_cols = [col for col in object_cols if set(X_valid[col]).issubset(set(X_train[col]))]

    bad_label_cols = list(set(object_cols) - set(good_label_cols))
`

Exercise done till 3(a)
* For large datasets with many rows, one-hot encoding can greatly expand the size of the dataset.
* Hence one-hot encoding requires relatively low cardinality columns.
* For higher cardinality, drop columns or use ordinal encoding.

3(b)
* If a column has 100 different possible categories, one-hot encoding will require 100 different columns to represent that column. Increase in dataset size = (no_of_rows * 100) - no_of_rows.