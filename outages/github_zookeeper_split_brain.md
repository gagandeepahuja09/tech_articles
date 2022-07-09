**Dissecting Github Outage - The Second Leader Problem**

**Kafka**
* Each Kafka topic can have multiple partitions.
* Kafka is not a single node cluster.
* It has multiple nodes(brokers).
* Each partition of a particular topic has a leader and a replica.
* A broker can have a leader of one partition and a replica of another partition.
    * This is how Kafka is able to sustain high read and write load across the cluster.

**Responsibilities of ZooKeeper for Apache Kafka**
1. Controller or Leader election:
    * Does the leader election and manages this information.
    * Takes care of assigning the new leader if the leader goes down.
    * Hence it acts as a brain.
2. Cluster Membership:
    * Manages which nodes are a part of the cluster.
3. Topic Configuration:
    * Manage the following:
        * List of topics.
        * No. of partitions for each topic.
        * Location of replica.
        * Leader node location.
4. ACL and quota:
    * Manages on who is allowed to read/write and how much.

* After v 2.8, Kafka doesn't have a true dependency on ZooKeeper. But the foundation of what Kafka uses internally still remains the same.