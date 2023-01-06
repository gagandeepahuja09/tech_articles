**Dynamo: Highly Available Key Value Store**
* In order to provide high availability, Dynamo *sacrifices consistency* under certain failure scenarios.
* Makes extensive use of:
    * Object versioning.
    * Application-assisted conflict resolution.

* Many use-cases which only need primary key access to the data. eg: best seller lists, shopping carts, customer preferences, session management.
* Data is *partitioned and replicated* using *consistent hashing* and consistency is facilitated by object versioning.
* *Consistency* is facilitated by *object versioning*.
* *Consistency among replicas* => *Quorum-like technique* + *Decentralized replica synchronization protocol*.
* *Failure detection and membership* => *Gossip-based protocol*
* *Completely decentralized with no manual administration*. Storage can be added or removed without requiring any manual partitioning or redistribution.
* Using this, session state application handles hundreds of thousands of concurrently active connections.

**Background**
* Most of the services only store and retrieve data by primary key and do not require the *complex querying and management* functionality provided by RDBMS.
* Problem:
    * Complex querying
    * Complex management: skilled personnel
    * Expensive hardware (why?)
    * Replication limitations
    * Partitioning schema flexibility limitations
    * Choose consistency over availability
* Dynamo   
    * Simple key/value interface.
    * Highly available.
    * Clearly defined consistency window.
    * Efficient in resource usage
    * Simple scale-out scheme.

**System Assumption And Requirements**
1. **Query Model**
    * State stored as binary objects. (blobs)
    * No operation spans multiple data item. Do RDBMS requirements.
    * Objects are relatively small. (< 1MB)

2. **ACID Properties**
    * ACID ==> poor availability.
    * Provides no isolation guarantees. (isolation levels ==> compromise on speed)
    * Permits only single key updates.

3. **Efficiency**
    * The system needs to function on a commodity hardware infrastructure.
    * Amazon has stringent SLA ==> p99.9
    * Tradeoffs are in *performance, cost efficiency, availability and durability guarantees*.

4. **Other Assumptions**
    * Only used by Amazon's internal services: no security requirements for authN, authZ.
    * Each service uses its distinct instance of Dynamo: initial design targets a scale of up to 100s of storage hosts.

**2.2 SLA**
* Each and every dependency must deliver with even tighter bounds. (because also need to take the network calls into consideration).
* SLA must include:
    * Client request rate distribution.
    * Expected service latency.
    * eg. p99.9 response of 300ms for a peak client load of 500 rps. 
* Customers with longer histories would have more processing times impact p99.9. These will be one of the most important users.
* Why not even higher percentile? Cost analysis showed much more higher increase in cost as compared to performance.

**2.3 Design Considerations**
* Traditional systems: sync replica: strongly consistent.
* Async replication: optimistic replication technique where changes are allowed to propagate to replicas in the background and concurrent, disconnected work is tolerated.
    * Problem: it can lead to conflicting changes which need to be resolved.
* *When should be conflicts be resolved, during reads or writes?*
    * Traditional systems reject writes if the data store cannot reach all of the replicas at a given time.
    * Dynamo: always writeable.
        * Cannot reject customer updates resulting in poor customer experience.
        * Push the conflict resolution to the reads so that writes are never rejected.