# Package Manager
* Helm is a package manager for k8s.
* It's job is to package YAML files and distributed them in public and private repositories.
* Let's say that we want to additionally deploy ELASTIC stack in the cluster that our application will use to collect its logs.
* We will need a lot of k8s objects for doing this: StatefulSets, ConfigMap, Secret, k8s Users with Permissions, Services.
* Building and testing this will take a lot of time.
* Since Elastic Stack deployment is pretty much the standard, other people will have to do the same.
* So it is better that someone created those YAML files, packaged them and made them available in a repository.
* This bundle of YAML files is called helm chart.
* These are available for most database, monitoring tools which have complex setup.

# Templating Engine
* We would be having multiple template values like request memory and CPU which could be different in stage and production.
* We can also use for things like the commit_id in order to make it configurable.
    * namespace/templates
    * namespace/values.yaml
* These values can be changed via a yaml file or via --set flag.
* This is quite practical in case of CI/CD as we can replace those values on the fly.

# Helm Chart Structure
* namespace/
    Chart.yaml
    values.yaml
    charts/
    templates/
* Chart.yaml: Meta information about the chart. `name`, `version`, list of `dependencies`.
* Example of dependencies:
    * your service internal pod (dark pod): only meant for testing by developers. The actual service should be up and running for this.
    * Some ephemeral DB.
    * Some other services which should be up and running for this.
* chart: for storing chart dependencies: if this chart is dependent on other charts. (not clear)
* `helm install <chartname>`: Templates will be filled with the values.yaml which can then be deployed to k8s.
* *How does helm ensure that the values are overriden by production or stage specific values.yaml?*
    * We can pass in the flag that we want a specific file to be taken as priority: `helm install --values=prod/namespace/values.yaml`

# Release Management
* Latest helm version: 3
* In helm 2, there was a server tiller which was setup in the k8s cluster which would create the k8s object from the yaml files.
* Tiller used to keep a history of each configuration sent by the client, hence providing release management via helm install, helm upgrade, helm rollback.
* *Downsides*: Tiller has too much power (too many permissions) inside k8s cluster for creating, updating and deleting resources. 
* In helm3 tiller was removed and there is only a helm binary now. This solves the security concern but makes it more difficult to use.