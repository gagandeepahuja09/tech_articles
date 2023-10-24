* Cross-validation for better measures of model performance.
* ML is an iterative process.
* We took a data-driven approach for selecting the features as well as model to use.
* There are still some drawbacks to this approach. Our model might have done well on a set of 1000 rows, but it might be inaccurate on another set of 1000 rows.
* Larger validation set: less randomness or noise in our ML model.
    * We can't do that at the expense of removing rows from training set.

* **Cross Validation**: 
    * Let's say we divide the data into 5 folds: f1, f2, ..., f5.
    * fi ==> test, rest validation for each i.
* *Small datasets*:  
