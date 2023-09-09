* *What is the request flow of a k8s request?*
    * Some user hits the k8s API through the kubectl command.
    * Goes to API server and the changes are saved in etcd.
* There is also authentication and authorization (RBAC)
    * If we want to do additional validations or mutations before this save to RBAC, we can use admission controller which are implemented via webhook.
    * *Question: is our API called? where is it placed?*
* *Two kinds of admission-controllers: validating and mutating*
    * /validating: Example:
        * certain configuration should always be there. Like: CPU and Memory should always be less than x and y else reject these.
        * Certain annotations must always be present. Like email of the user if we have some B2B.
    * /mutating       
        * Add default values of these, if not specified.
        * Service Mesh is also a great example of mutation.
        * We don't have to change for each and every application (namespace) for setting up a side-car each time.
