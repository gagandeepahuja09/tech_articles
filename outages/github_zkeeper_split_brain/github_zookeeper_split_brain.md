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

**Incident: What Happened?**
* ZooKeeper nodes were getting provisioned as part of routine upgrade. This happens during version upgrade, OS patch, security patch, etc. During this, new nodes are added and old ones are removed.
* New nodes being added "too quickly" lead into another leader election.
* When new nodes were added, it lead to a scenario where the majority of the nodes were not able to quickly discover the leader.
* Hence they triggered a leader election and elected a new leader.
* This led to a situation where there were 2 logical clusters each having multiple followers and a leader.
* There were a lot of Kafka brokers which were connect to the old logical zookeeper cluster.
* A single broker got connected to the new Zookeeper cluster and elected itself as the controller(leader) for a topic as it was not aware of the leader as it could not talk to the old cluster.
* This led to there being multiple leaders for a Kafka topic.

* Kafka needs to get the information from Zookeeper regarding the node on which it should write.

* When clients are connecting to Zookeeper for Kafka details, they are getting conflicting information. In such cases where the client receives conflicting information, it drops the writes.

* Note: If there were multiple brokers added to the new logical cluster, it could have resulted in the write getting completed.

**Recovery**
* Zookeeper does a periodic heal. It auto-detects this inconsistency over-time and auto-heals. 
* We can also take actions manually to fix it. eg. Killing the second logical cluster.

*What got affected*
* The Kafka cluster where it happened handled internal background job.
* So, did they loose any jobs since the writes must be failing?
    * No, because of DLQ.
    * Due to this there was some delay but no data loss, which is fine for internal systems. 

**Fallback Queues**
* A standard architecture requires us to have Deadletter queues.
* Idea: If unable to put the message in main queue, put it in DLQ which are processed later. DLQ should generally be cheap, usually a broker and not a stream.

**Important Learnings**
1. Having a DLQ is a must.
2. Consumers should be idempotent.
3. Clients and consumers should have retries.
4. Automate cluster provisioning with a jitter.