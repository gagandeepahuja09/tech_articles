* To acheive high availability, dynamo sacrifices consistency under certain failure scenarios.
* Amazon used SOA with 100s of services.
* Many of the Amazon's services only required primary-key access to a data store. Relational databases would limit the scale of availability.

* Data is partitioned and replicated using *consistent hashing*.
* Consistency is facilitated by object *versioning*.
* The consistency among replicas during updates is maintained by a quorum-like and a decentralized replica synchronization protocol.
* It is completely decentralized with minimal need of manual intervention. Storage nodes can be added or removed without requiring any manual partitioning or redistribution.
* Dynamo is highly available with a clearly defined *consistency window*.

* In Amazon, services have stringent latency requirements which are measured at p99.9.

**2.3 Design Considerations**
* *Availability can be increased by using optimistic replication techniques*, where changes are allowed to propagate to replicas in the background and concurrent, disconnected work is tolerated.
* We need to resolve conflicts in such scenarios. Problem: when (reads/writes) to resolve them and who resolves them.
* Most traditional data stores handle conflict resolution during writes and keep the read complexity simple. Writes could be rejected if it didn't reach all of the replicas in a given time.
* Dynamo on the other hand is known to be *highly available for writes*.
    * Why? Rejecting customer updates could result in a poor customer experience.
* This requirement forces Dynamo to push the complexity of conflict resolution to the reads in order to ensure that writes are never rejected.
* Who does the conflict resolution? Application or Database? Application far more flexible, Db only has option of LWW.

**4.6 Handling Transient Failures: Sloppy Quorums with Hinted Handoff**
* Traditional quorums prefer consistency over availability.
* *Sloppy quorums*: Write operations are performed on the first N healthy nodes instead of the first N nodes. (nodes encountered while walking the consistent hashing ring). 
* Example: Node A is temporarily down. During writes, the replica that would have normally lived on A will now be sent to node D.
* *Hinted handoff*: 
    * The replica sent to D will have a hint in its metadata that suggests which node was the intended recipient of the replica. 
    * Hinted replicas are kept in a separate local database that is scanned periodically and upon detecting that owner node has recovered, it is delivered to the owner.
* Highest level of availability: W=1 which means that a write is accepted as long as a single node has durably written the key to its local store. In practice, we set a higher value of W.

* *Availability across datacenters*:
    * Datacenter failures could be due to: power outages, cooling failures, network failures, natural disasters.
    * Dynamo is configured such that each object is replicated across multiple data centers.
    * These datacenters are connected through high speed network links.

**4.7 Handling Permanent Failures: Replica Synchronization (Anti-entropy)**
* Hinted replicas could become unavailable before they are returned to the original replica node.
* *Merkle trees* are used to:
    * detect the inconsistencies between replicas faster.
    * minimize the amount of transferred data.
* Merkle tree is a hash tree:
    * Leaves are the hashes of values of individual keys.
    * Parents are the hashes of their children.
    * Each branch can be checked individually without downloading the entire tree set. We only need to check the hashed value of the root of the branch.
    * If hash values of 2 roots are equal, then they are in sync.
    * We can continue the process recursively to find the parts which are not in sync.
* How Dynamo uses Merkle trees:
    * Each node maintains a separate Merkle tree.