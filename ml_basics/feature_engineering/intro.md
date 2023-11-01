* *Mutual Information*: Determine which features are the most important.
* Inventing new features.
* *Target encoding*: Encoding high-cardinality categoricals.
* *K-means clustering*: Creating segmentation features
* *Principal component analysis*: Decomposing a dataset's variations into features.

**Goal of Feature Engineering**
* Making data better suited to the problem at hand.
* Improve model's predictive performance.
* Reduce computational or data needs.
* Improve interpretability of the results.

**A Principle of Feature Engineering**
* For a feature to be useful, it must have a relationship with the target that the model is able to learn from.
* *Transformations*: 
    * Predicting price from length of land.
    * Fitting a linear model directly to length gives poor performance. We can do better if the relationship is not linear.
* *Derived features can add a lot of value but how to identify them?*.
    * Correlation tests, chi-square tests.
    * Domain knowledge

**Example**
* While cooking, for a recipe, the relative amount is more important than the absolute amount. Hence, important ratios can add a lot of value.

`
    X["FCRatio"] = X["FineAggregate"] / X["CoarseAggregate"]
    X["AggCmtRatio"] = (X["FineAggregate"] + X["CoarseAggregate"]) / X["Cement"]
    X["WaterCmtRatio"] = X["Water"] / X["Cement"]
`