# Setup Prometheus on a K8s Cluster
* 2 main components in Prometheus: Server and Alert Manager
* Server further has 3 components: 
    * *HTTP Server*: accepts PromQL queries
    * *Time Series Database*: stores metrics data
    * *Data retrieval Worker*: pulls metrics data

# How to deploy?
* *Option 1: Create all configuration files yourself and execute them in the right order*
* *Option 2: Use an operator*
    * Multiple components will be created: StatefulSet, Deployment, Service.
    * The operator manages all of the components as a single unit.
    * You will have the watching logic and the reconciliation loop for this operator which would already be implemented by the Prometheus operator.
* *Option 3 (Most preferred): Using helm chart to deploy operator*
    * Helm will do the inital setup
    * Operator will then manage the setup.