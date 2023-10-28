* **Data Leakage**: When training data contains certain information which won't be available in production.

* **Target Leakage**
    * When you include data that won't be available at the time you make prediction.
    * It is in terms of *timing or chronological order* in which the data becomes available and not whether a feature helps make good predictions.
    * Eg: `took_antibiotic_medicene` is frequently changed after the prediction_target: got_pnuemonia is determined.
        * model would predict that when took_antibiotic_medicene=False, got_pnuemonia=False.
    * And when deployed in real world, most patients first time won't have taken any medicene.

* **Train-test contamination**
* 