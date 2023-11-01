* Measure relation b/w two quantities, like correlation.
* Its adv: detects any kind of relationship and not just linear relationships.
* MI is a logarithmic quantity.
* 0 value: no relation b/w the 2 quantities.
* MI gives an indication of the degree of uncertainity in determinig the target from the feature.
* *MI is a univariate metric*: It is possible that a feature can be very informative when interacting with other features but not so informative all alone. *MI can't detect interaction b/w features.*

**Example**
* Predict car's price.
`
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    import seaborn as sns

    plt.style.use("seaborn-whitegrid")
    df = pd.read_csv("autos.csv")
    df.head()
`

* Scikit algorithm for MI treats discrete features differently from the continuous ones. We need to explicitly tell that in the constructor.
    * Generally numeric are continuous and categorical are discrete.
    * float is generally continuous.
* Ordinal encoding and identifying discrete features
`
    X = df.copy()
    y = X.pop("price")

    # Ordinal encoding
    for colname in X.select_dtypes("object"):
        X[colname], _ = X[colname].factorize()

    # Assumption: should be confirmed for your use case
    discreted_features = X.dtypes == int
`