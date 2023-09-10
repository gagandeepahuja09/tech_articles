* *Securing our cluster*
    * RBAC: role of people who have access to the cluster
* CI/CD pipeline that points to k8s cluster and is the only way that code can be pushed to k8s cluster.
    * Add processes and security checks like vulnerability detection and intrusion detection via DaemonSet.

* *Monitoring in our cluster*
    * Installed via DeamonSet.
    * fluentd, Jaeger

* *Failover*
    * Clusters in more than one region. 