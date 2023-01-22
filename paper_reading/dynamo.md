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
* *Who performs conflict resolution: data store or application?*
    * Choices are limited if the resolution is performed by the data store. eg: LWW (last write wins).
    * Since the application is aware of the schema, it can decide on the basis of user experience. Eg: shopping cart: merge and show.
    * Both options provided.

* *Incremental Stability*: Application should be able to scale out one storage node at a time, with minimal impact on operators of the system and the system itself.
* *Symmetry*: 
    * Every node should have same set of responsibilities as its peers.
    * It simplifies the process of *system provisioning and maintainence*.
* *Decentralization*:
    * Simpler, more scalabable, available system.
* *Heterogeneity in Infrastructure*:
    * Work distribution must be proportional to the capabilities of the individual servers.
    * Helps in adding new nodes with higher capacity without having to upgrade all nodes at once.

**3. Related Work**

**3.1 Peer to Peer Systems**
* O(1) routing: each peer maintain enough routing information locally so that it can route requests to the appropriate peer within a constant no. of hops.

**3.3 Main Characteristics**
1. Always writeable - Updates are not rejected due to *failures* or *concurrent writes*.
2. Single administrative domain where all nodes are assumed to be trusted.
3. Applications using Dynamo don't require support for hierarchical namespaces (file systems) or complex relational schema (traditional databases).
4. p99.9 ==> few 100 ms. To meet stringent SLAs, it is imperative to avoid routing requests through multiple nodes.
    * Multi-hopping increases variability in response times.
    * Zero-hop DHT. Each node maintains enough routing info to route request to the appropriate node directly.

**4 System Architecture**
* System needs to have scalable solutions for load balancing, membership and failure detection, failure recovery, replica synchronization, overload handling, state transfer, concurrency, job scheduling, request marshalling, request routing, system monitoring, alarming, configuration management.

* Core techniques discussed: partitioning, replication, versioning, membership, failure handling and scaling.

**4.1 System Interface**
* Two operations exposed: get and put.
* *get(key)*: Returns a single object or a list of objects with conflicting versions along with a *context*.
* *put(key, context, object)*
* *Context*:
    * System metadata like object version.
    * Opaque to the caller. (who is the caller?)
    * It is stored along with the object so that the system can identify the validity of the context object.                            
* MD5 hash is applied to the key to generate a 128-bit identifier to determine the storage nodes responsible for serving the key.   

**4.2 Partitioning Algorithm**
* *Incremental scaling requires dynamic partitioning*.
* Common technique: consistent hashing.

* *Consistent Hashing*: 
    * Output range of a hash function is treated as a fixed circular space or *ring*.
    * i.e. Largest value wraps around the smallest value.
    * Each node is assigned a *random value* within this space which denotes its *position*.
    * In order to map a key to a position, we take the hash (eg. MD5 hash) of the key and by walking clockwise, find the node with the just greater value. (we could implement consistent hashing using binary search).
    * Each node becomes responsible for the region b/w it and its predecessor.
    * **Principal Advantage**: The arrival and departure of a node only affects its immediate neighbours and other nodes remain unaffected.

* *Challenges with the basic consistent hashing algorithm*:
    * *Random position assignment* of nodes leads to *non-uniform data and load distribution*.
    * Oblivious to the *heterogeneity in the performance of nodes*.

* *Solution: virtual nodes*
    * Instead of assigning a node a single point in the ring, each node gets assigned multiple points in the ring.

* *Advantages of virtual nodes* 
    * If a node becomes unavailable (due to failure or routine maintainence), the load handled by this node is evenly distributed across all the remaining available nodes.
    * When a node becomes available again, or a new node is added to the system, the newly added node accepts a roughly equivalent amount from each of the other available nodes.
    * The no. of virtual nodes a node is responsible for can be decided on the basis of its capacity, accounting for heterogeneity in the infrastructure.

**4.3 Replication**
* Required to achieve *high availability and durability*.
* Each data item is replicated at N hosts. N is a parameter *configured per-instance*.
* Each key k is assigned to a *coordinator node*.
* The coordinator is in charge of replication of the data items that fall within its range (N-1 successor nodes).
* Each node is responsible for the region b/w it and its Nth predecessor.
* *Preference List*: List of nodes responsible for storing a particular key.
* *Membership Detection*: Every node should be able to determine what all nodes should be in the list for a particular key.
* Note: All N should be physical nodes and not virtual nodes.

**4.4 Data Versioning**
* Eventual consistency. There is a bound on the update propagation times. However, under certain failure scenarios (eg. server outages or network partitions), updates may not arrive at all replicas for an extended period of time.
* Applications like shopping cart can tolerate such inconsistencies.
    * If the latest state is unavailable to the user and the user makes a change to an old state, that information is still useful and should be preserved.
    * It should supersede the currently unavailable latest state and should be maintained as a new version.
* Both add to cart and delete items from cart or any update on cart ==> all are put requests on Dynamo.
* Certain failure modes can result in having even more than 2 versions of the same data.
    * Application developers will need to design application that keeps the reconciliation in mind. We don't want to loose any update.

**Causality via Vector Clocks**
* It is a list of (node, counter) pairs.
* We can determine whether 2 versions are on parallel branches or have a causal ordering by examining their vector clocks.
    * If the counters of the first object's clock are <= all of the nodes in the second clock, then the first is the ancestor of second and can be forgotten.
    * Otherwise the 2 changes are considered to be in conflict and require conciliation.
* When a client wishes to update an object, it must specify which version it is updating.
    * put(key, context, object) ==> context contains the version information.
    * get(key) ==> will return all leaf objects.
* Overwritten data (D1, D2, D3, D4) can be garbage collected.
* There is no causal relation b/w D3, D4. One has Sy value higher while the other has Sz value higher. In such cases, both versions are presented to the client.

* *Handling vector clock size*: 
    * If too many servers are coordinating the writes to an object, then the size of the vector clock can grow very quickly. 
    * In practice, this should not happen because writes will only happen by the top N nodes in the preference list.
    * In case of network partitions or multiple server failures, nodes that are not in the top N preference list can also contribute to the writes.
    * *Clock Truncation Scheme*: 
        * Along with maintaining a (node, counter) pair, we also maintain, we also maintain a timestamp which indicates when the node updated the item.
        * Once the no. of items ie (node, counter) pair reach a threshold, we remove the oldest item.
        * Could lead to inefficiencies but they haven't solved for it due to no issues encountered on production.

**Execution of get and put operations in failure-free environment**
* *Request routing*
* *Consistency among replicas*:
    * Quorum: R + W > N. R and W are configurable values.
    * R (or W) is the minimum no. of nodes that must participate in a successful read (or write) operation.
    * The latency of a get (or put) operation is determined by the the slowest of the R (or W) replicas.
    * Hence the ideal value of R + W is N + 1. Else it will add to the latencies. 
    * *Write Path*
        * Upon receiving a put() request for a key, the coordinator generates the vector clock for the new version and writes the new version (along with the vector clock) locally.
        * The coordinator then sends the new version (along with the vector clock) to the N highest-ranked reachable nodes.
        * If at least W-1 nodes respond, then the write is considered successful.
    * *Read Path*
        * Similar to write path, request goes the N nodes from pref list and waits for R-1 responses.
        * If there are multiple versions, it returns causally unrelated versions.
        * Divergent versions could be reconciled at the application layer.
    * *Question: What if W writes are not possible? Do we handle rollbacks for the successful writes?*

**Handling Failures: Sloppy Quorums And Hinted Handoff**
* *Tradition Quorum*: Reduced availability during network partitions. Might reject writes if W/R writes/reads are not possible.
* *Sloppy Quorum*: Read and write operations are performed on the first N healthy nodes, which may not always be the first N nodes encountered while walking the consistent hashing ring.
* How will one of the actual first N node get the data if it was not written due to the node not being healthy at that time?
* *Hinted Handoff* helps with this:
    * Assume that due to A being down, it was sent to D.
    * D will have a hint in its metadata that suggests which node was the intended recipient of the data (A in this case).
    * Nodes that receive hinted replicas will keep them in a separate local database that is scanned periodically.
    * Upon detecting that A has recovered, D will attempt to deliver it to A. Upon successful transfer, D can delete the data from its local store.

* In order to have the highest level of availability, the value of W should be 1, which means that even if a single node is healthy and able to durably write the key to its local store.

* In practice, Dynamo sets a higher value of W to meet the desired level of durability
* Question: How is durability compromised if the write was successful to one node?

* Dynamo targets multi-datacenter level durability.
    * The preference list of a key is constructed such that the storage nodes are spread across multiple data-centers.
    * The datacenters are connected through high-speed network links. 

**Handling Permanent Failures: Replica Synchronization**
* Hinted replica nodes can become unavailable before they are returned to the original replica node.
    * (*Not able to clearly visualize how the above problem is fully solved.*)
* To handle this and other threats to durability, Dynamo use Merkle-trees for synchronization. 
* Merkle-tree:
    * Binary hash tree. Leaf nodes are hashes of the keys.

**4.8 Membership And Failure Detection**

* *4.8.1 Ring Membership*
* A node outage rarely signifies a permanent departure (often transient) and hence should not result in rebalancing of the partition assignment or repair of the unreachable replicas.
* (Question: how are permanent failures detected? If a node is unhealthy, it could be a partial failure or a permanent failure. This might need to be determined via logs?)
* Hence, the process used is partially manual. An administrator uses CLI/browser to issue a change to join a node to a ring or remove a node from a ring.
    * The node that serves the above request writes the membership change and its time of issue to persistent store. The membership changes form a history.
    * *Gossip-based protocol*: Each node contacts a peer chosen at random every second and the two nodes effectively reconcile their persisted membership change histories.
* When a node starts for the first time, it chooses its set of virtual nodes and maps the relation (node to virtual node). The mappings are reconciled during the same gossip communication that reconciles membership information.
    * Hence partitioning and placement information are both reconciled via gossip-based protocol.
    * This allows each node to forward request to the appropriate virtual node directly.

* *4.8.2 External Discovery: Solving Split Brain*
* The administrator could add two nodes (A, B) to join the ring and neither would be immediately aware of the other.
* This problem is solved by adding seed nodes: which are discovered through external mechanism like reading a static configuration file.
* This results in all nodes being aware of the seed nodes.
* 

**5. Implementation**
* Each storage node has 3 main software components:
    * Request coordination
    * Membership and Failure Detection
    * Local Persistence Engine

* *Local Persistence Engine*:
    * Built such that different nodes storage engines can be plugged in.
    * Reason for choosing pluggable storage engine: application owners can choose the engine best suited for their access patterns.
    * Engines in use by Dynamo: 
        * BDB (Berkeley DB) Transaction Data Store (used for majority of the cases).
        * BDB Java Edition
        * MySQL
        * In-memory buffer with persistent backing store.

* *Request coordination*
    * The message processing pipeline uses SEDA. (Staged Event Driven Architecture)
        * (Question: how is staging useful for performance in the CS world? is there some proof?)
    * Each client request results in the creation of a state machine on the node that received the client request.
    * The state machine contains the logic for:
        1. Identifying the nodes responsible for a key.
        2. Sending the requests.
        3. Waiting for responses.
        4. Potentially doing retries.
        5. Processing the replies.
        6. Packaging the response to the client.