* We don't want developers to be able to see into each others work.
* We could have certain nodes and operations not be accessible to everyone.
* When we have different roles like developers, operators and cluster creators, it becomes even more important.

* A role generally defines a verb and a noun.
    * Verb (Action): get, list, update
    * Noun (Resources): pods, volumes

* Let Pods, Volumes, Deployments, etc, Role is also a RESTful resource.
    * We can also create them ourselves using a YAML file.
    * We can create custom roles also.
* By itself, the role doesn't grant any permissions.
* RoleBinding: mapping of a role for an individual or group.
* Kinds of resources in k8s:
    * Namespaced resources
        * Service or a pod which exists only within a namespace.
    * Cluster resources: eg Customer Resource Definition.
        * It is defined for the entire cluster.
* We can also limit resources at a namespace level:
    * Having access to resources at a namespace level.

* *Two type of RoleBinding*
    * ClusterRoleBinding: provides permissions for the entire cluster (both namespaced and cluster resources). They are very powerful, so we have to be very careful while using them. They not only apply to existing namespaces, but also future namespaces.
        * Cluster object/resource
        * */clusterolebinding*
    * RoleBinding: provide permission only for namespace.
        * Namespace object
        * */my-team/rolebinding*