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