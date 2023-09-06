Source: https://www.youtube.com/watch?v=ZuIQurh_kDk&ab_channel=CNCF%5BCloudNativeComputingFoundation%5D

*Why Kubernetes?*
* We have to start with going to the time when docker was also not there. The only way to deploy application was to run them directly on machines and virtual machines.
* Deployments were not repeatable, consistent and deployment requiring a lot of manual effort.

* How does Kubernetes coming into picture? Docker is a great technology but how do we scale the deployments. We can't go and SSH into each machine and then deploy the docker container.
* Kubernetes is a container orchestration tool that helps solve problems like these.

# Key design principles

## *Principle 1: Use declarative syntax and approach over imperative*
* Rather than telling what exacts steps need to be done, tell what is the desired end-state.
* *What is the main advantage of this approach?*
    * If we tell the steps, then we need to be wary of the initial state as well.
    * In case of imperative, failure needs to be handled explicitly by defining business logic on what needs to be done in such cases.
    * *Declarative syntax provides automatic recovery.*
    
## *Principle 2: Kubernetes control plane is transparent. It has no internal APIs*
* The immediate thought on building something like k8s would be to have a master node (or master nodes) responsible for bringing up the pods and consistently checking if the current state of the pods matches the desired state.
    * With this approach, the possible failure cases are endless as in a client-server architecture.
    * Either of the nodes can be down. There can be some temporary blip. (will we retry?)
    * There can be timeout related issue where server got the changes but didn't respond in time. 
    * The master node will become inherently *complex, brittle and impossible to extend*.
        * It will have to keep on monitoring each and every node and will also have to play catchup if the state deviates.
        * For each new use-case, we might require introducing changes to how master nodes also work.

* The APIs that k8s exposes to the end user are exactly the same as the APIs that all k8s internal components use.
* Instead of having the decision of what needs to be done for each being centralized and sent out to each and every node, every component is responsible for its own health and keeping itself running.
* Whenever a component comes up, it goes to the API server to figure out what it should be doing.
    * *This helps in automatic recovery*: We don't need to custom, failure or error handling logic. Whenever a node comes back up, it knows the exact desired configuration by checking k8s master API server.
    * *This is level-triggered vs edge-triggered*: In case of edge-triggered, we need to listen for changes via events. (imperative.)
* *What if the k8s master nodes go down or master API server? Won't that be a SPOF?*
    * By distributing the responsibility, we are making the system more reliable and extensible.
    * If master was calling every node, it was definitely a SPOF.
    * With the k8s model, the nodes continue to operate at the last state that they saw.

* *Extensible*
    * Very easy to extend and build custom implementations.
    * Example, we can write our custom scheduler.