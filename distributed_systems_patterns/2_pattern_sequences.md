**Fault-Tolerant Consensus**
* Consensus refers to a set of servers which agree on:
    * Stored data
    * The *order* in which the data is stored.
    * *When to make that data visible to the clients*.

* We are assuming a *crash-fault* model here, which means: cluster nodes stop working and crash when any fault happens.
* Paxos describes a few simple rules to use *two-phase execution*, *quorum* and *generation clock* to acheive consensues across a cluster of nodes even when there are *process crashes, network delays and unsynchronized clocks*.

* When data is replicated across cluster nodes, *acheiving consensus on a single value is not enough*. All the replicas need to reach agreement on all the data. This requires *executing paxos multiple times, while maintaining strict order*.
* *Replicated log describes how basic paxos can be extended to achieve this.* Acheiving consensus on a single request is not enough. Each replica needs to execute requests in the same order, otherwise different replicas can get into a different final state, even if they have consensus on an individual request.
* The key implementation is to replicate WAL on all the servers to have a replicated log.


**Pattern-sequence for implementing replicated log**
* Durability guarantees via the WAL pattern.
* WAL is divided into multiple segments using the *segmented log*. This helps with log cleaning which is handled by a low-water mark.
* Fault-tolerance is provided by replicating the WAL on multiple servers.
* The replication is managed using Leader and Followers pattern and *quorum* is used to update the *high-water mark* to decide which values are visible to the clients.
* *All the requests are processed in strict order, by using **Singular Update Queue** *.
* The order is maintained while sending the requests from leaders to followers using *Single Socket Channel*.
* To optimize for throughput and latency over a single socket channel, *Request Pipeline* can be used.
* Followers know about the availability of the leader via the *Heartbeat* received from the leader. 
* If the leader is temporarily disconnected from the cluster because of *network partition*, it is detected by using *generation clock*. 
* *Follower reads* allows handling read requests from follower servers.

**Kubernetes or Kafka Control Plane**