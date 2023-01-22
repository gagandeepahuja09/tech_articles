**Mastering Chaos: A Netflix Guide To Microservices**

*An Evolutionary Response*
* *Separation of concerns*
    * *Modularity, encapsulation*: Many of the functionality is encapsulated so that the interactions are limited.

* *Scalability*
    * Horizontal scaling, workload partitioning

* *Virtualization and Elasticity*
    * It is much harder to manage microservices if we are not doing this in a virtualized environment.
    * Automated operations, on demand provisioning.

**Challenges And Solutions**
4 Layers
* Dependency
* Scale
* Variance
* Introducing Changes

**Dependencies**
Use Cases

**Intra-service requests**
*Problems* 
* N/w latency, congestion, failure
* Logical or scaling failure (at the downstream service)
    * Cascading failures
* Hystrix:
    * Structured way of handling timeouts and retries (backoffs)
    * Fallbacks
    * Circuit breaker
* How do you know if it works?
    * Inoculation in Biology.
    * Fault Injection Testing (FIT): 
        * Can be done using synthetic transactions or % of live traffic.
        * We want to test it no matter how we call the service.
        * With so many permutations and combinations, how do we constrain testing scope?
* *Availability*: Each service has 4 9s of availability: it can be down for 53 minutes in an year.
    * If for our service, we have 10 microservices with 4 9s of availability, aggregating would give 3 9s of availability for the entire service.
* Hence categorizing *critical microservices* is crucial. This helps both in availability and FIT perspective. We will apply FIT such that all the critical services are covered.


**Client Libraries**
* Todo
* For common access patterns.

**Data persistence**
* We should first start with CAP theorem.
* *CAP Theorem*: In the present of n/w partition, we mush choose b/w consistency and availability. Let's say a service writes the same data to 3 different databases. What if you can't reach one of them? Do you fail or write to the ones you can write to. 

**Infrastructure**
* Multi-region strategy.

**Scale**
**Stateless Services**
* Not a cache or a database.
* No instance affinity. There is no mapping that such kind of requests would go to only such kinds of nodes.
* Loss of a node is a non-event. We can spin up a new instance very quickly if one goes down.
* We might maintain frequently accessed metadata in memory.

* *Auto-scaling groups*: 
    * We have min and max size and can scale-out as needed.
    * *Compute-efficiency*: We are making use of on-demand capacity.
    * *Node failure*: Replaced
    * Traffic spikes and performance bugs can be solved to a certain extent till we fix any bugs or improvements.

* *Surviving Instance failures*: Chaos monkey.

**Stateful Services**
* Cache or database or custom apps which hold large amount of data.
* Instance affinity
* Loss of a node is a notable event. 

**Dedicated Shard - An Antipattern**
* Having dedicate nodes for customers, only one copy of the data - SPOF. 
* Didn't have proper hystrix setting, bulk-heading, isolation of thread pools => one node down and the entire netflix went down.
* *Redundancy is fundamental* (2 kidneys, 2 lungs).
* EVCache is used for redundancy: it is also sharded. Replicated across different availability zones. 