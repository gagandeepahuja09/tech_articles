* Finding the features that best describe the target.
* *MAE: Mean Absolute Error* => calculated by mean of *difference in actual and predicted value.*

**Mutual information**
* It can detect any kind of relationship, while mutual information only detects linear relationship.
* Logarithmic value
* Measure of the extent to which knowledge of one quantity reduces uncertainity about the other.
* MI = 0 ==> independent
* It can help to tell the relative potential of a feature as a predictor of target by itself.
* It is possible for a feature to be very informative when interacting with other features but not so much all alone. MI can't detect interactions b/w features. It is a *univariate metric*.

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

plt.style.use("seaborn-whitegrid")
df = pd.read_csv("../../xyz.csv")
df.head()

* The scikit algo for MI treats discrete and continuous values differently.
* floats and ints generally continuous.
* Categorical: discrete: give them label encoding.

X = df.copy()
y = X.pop("price")

* **Label encoding**: Converting categorical data (text-based categories) into numerical values so that ML models can work with them easily.
    * *Why?*: 
        * Most ML models are based on mathematical, statistical operations.
        * Involve regular arithmetic operations as well complex mathematical functions.