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