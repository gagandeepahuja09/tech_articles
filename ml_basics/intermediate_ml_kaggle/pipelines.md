* Keeping the data preprocessing and modelling code organized.

**Benefits**
1. *Clean code*: Accounting for training and validation data at each step can be messy. Pipeline helps with that.
2. *Fewer bugs*: There are fewer opportunities to missaply a step or forget a processing step.
3. *Easier to productionize*
4. *More options for model validation* 

* *Pipelines are nested*
    1. You can apply multiple steps of categorical transformer: this is a pipeline.
    2. You can apply multiple steps of preprocessing: numerical and categorical transformer. (made use of pipeline in step 1) via *ColumnTransformer* class.
    3. Preprocessor and model are also separate steps which can be bundled in the final pipeline.

**Step 1: Define Preprocessing Steps**
* ColumnTranformer class can be used to bundle different processing steps.

`
    from sklearn.compose import ColumnTransformer
    from sklearn.pipeline import Pipeline
    from sklearn.impute import SimpleImputer
    from sklearn.preprocessing import OneHotEncoder

    numerical_transformer = SimpleImputer(strategy='constant')

    categorical_transformer = Pipeline(steps=[
        ('imputer', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore'))
    ])

    preprocessor = ColumnTransformer(
        transformers=[
            ('num', numerical_transformer, numerical_cols),
            ('cat', categorical_transformer, categorical_cols),
        ]
    )
`

**Step 2: Define the model**
`
    from sklearn.ensemble import RandomForestRegressor

    model = RandomForestRegressor(n_estimators=100, random_state=0)
`

**Step 3: Create And Evaluate the Pipeline**
`
    from sklearn.metrics import mean_absolute_error

    my_pipeline = Pipeline(steps=[('preprocessor', preprocessor),
                            ('model', model)])

    my_pipeline.fit(X_train, y_train)
    preds = my_pipeline.predict(X_valid)

    print(mean_absolute_error(y_valid, preds))
`