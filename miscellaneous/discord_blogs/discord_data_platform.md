https://www.youtube.com/watch?v=yGpEzO32lU4&t=887s

* When a company scales, they adopt microservices architecture which leads to each service having separate database.
* With data being distributed across multiple databases, there emerges a need to unify that in order to extract insights out of it. 

**Why companies need a data platform?**
* Product insights.
* Business decisions and strategies.
* Power data science and train ML models.

* All the data is duplicated (typically using CDC pipeline) and stored in a centralized location - data warehouse / data lake.
    * Unified view of data / information.
    * Crunching stats / analytics.

**Discord's Data Platform - Derived**
**Challenges**
1. Unified view of multiple tables
    * We will require unifying data from multiple tables into a single table in order to get product insights out of it.
    * Can't we use joins? Apart from slowness, any other problem?
2. Non-relational data sources
3. Different data views for different end usecases (eg. product, insights, ML team all might require a separate view).