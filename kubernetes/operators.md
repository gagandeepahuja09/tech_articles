* Going back in history, there used to be operator and a punch card in computers. That operator used to do the jobs of an Operating System.

* K8s operator solves similar problems like OS in k8s for Stateful applications.
* Generally a DBA is required for running many DDL queries (create database), backup, schema migration.

* *How is this possible?*
    * It is highly extensible. 
    * It has a bunch of core APIs. But it also has primitives to be able to add new APIs while the system is running.

* An operator is also like a Pod. It might register an API like /databases/mysql.
    * This API allows a new API object to come into existence.

* *This operator is also self-healing*. It is going from CurrentState to DesiredState.
    * The backup or schema migration would be part of the desired state in that case.

***********************************************************************************

* k8s operator: https://www.youtube.com/watch?v=CK938sKNu4c&ab_channel=CNCF%5BCloudNativeComputingFoundation%5D
* The operator watches k8s API server for events.
* Whenever an event occurs that we care about, trigger the reconciliation loop that we implemented.
* Often the events that we are watching are custom APIs that we write (CRD: custom resource definition). But they don't necessarily have to be custom APIs, we can also watch for changes in Deployments for example.
* *Controller*: It is the part in the operator that implements the reconciliation logic.
* Operator can have one or more controllers.
    * It also does few other things like validating admission webhooks or mutating admission webhooks.
* Each resource in k8s has its own operator.

* When I apply a deployment resource, the deployment controller is watching for new deployment objects.
    * It's job is to create a ReplicaSet.