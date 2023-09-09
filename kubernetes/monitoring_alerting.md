* Kubernetes already comes with a lot of metrics available to us out of the box.
    * Which means we don't have to set up monitoring of the pods for CPU, Memory, etc.
    * All of these metrics are pushed to the k8s metrics server.
    * From there, they can be pushed out to cloud based monitoring like AWS cloudwatch or prometheus.
    * We can also push the metrics from code.
* We can also measure addition application specific metrics through a Service mesh.
* *Alerting*: Have alerting for user-experience.