* Fully-managed NoSQL database provided by AWS.
    * Fully-managed: we don't need to run and manage our own instances.
    * You cannot run it locally or on any other cloud.
* Key advantages: consistency, predictability and reliability.
    * Consistent performance in terms of response time. (from Mbs to Pbs to data) or if you are making concurrent requests (higher TPS).
    * Predictability in terms of billing: we will be charged on the basis of the no. of units of 4kB data we read and the units of 1kB data we write.
        * That is a much easier math and planning problem than the one based on CPU and RAM.
        * We might require running load tests otherwise.
        * We will be aware of the tps at which we are getting requests currently and can easily calculate on what would happen if it gets 2x / 4x.
    * Reliability:
        * Managed by AWS: you can take it down by firing high no. of queries. 
        * Multi-tenant system. Only reason that the DB can go down is when we can have a region-wide outage in AWS.

* Original Dynamo
    * Much simpler key-value data model. (no secondary indexes) DynamoDB has a richer data model.
    * Dynamo was run like a single-tenant system. Each team would run their own instance.
    * Dynamo: leaderless. Any of them can take writes, hence helps with availability but compromises with consistency.
    * 2022: DynamoDB released a new paper.
    * Symmetry and Shared-nothing architecture: Each server has the same job. Makes the job of maintainence very easy. true with Dynamo, not true with DynamoDB? DynamoDB is operating without being symmetric because because doing the maintainence at their scale makes sense because of ammortizing a large no. of users. 

**Write Path in DynamoDB**
* Shared-infrastructure.
* Each request to a fleet of load balancers which then goes to the request router.
* Request router is also a fleet of services which tells the partition to be used on the basis of the partition key.
* Each read and write request needs to have a partition key.
* Each partition will store a maximum of 10 GB of data.
* Each partition is replicated across replica groups. (3 replicas for each partition).
* Each replica will be in a separate availability zone. AZs are different data center within a region.
* Even if one AZ goes down, we have more replicas to serve the request.
* At any given time, one of the replicas is going to be elected as a leader.
* We will wait for quorum of writes.
* Partitioning key should usually be something meaningful. We should avoid auto incrementing id here (why?). Reason: we need that to be done by some coordinator itself to give out those value.
* Uuid might be fine. 
* DynamoDB doesn't provide that level of configurability where we can play around with changing the conditions of no. of consistent reads and writes.

**Read Path in DynamoDB**
* If we don't specify that we are looking for consitent reads, then it is going to by default (eventual consistency): 
    * LB layer -> Request Route layer -> partition metadata -> 3 different replicas: choose 1 of them for the read (randomly?).
    * Discount if we go ahead with eventually consistent read. (lag of the 3rd isn't much in most cases: 2ms).
    * Strongly consistent always hits the leader.

**Sort Key and Secondary Indexes**
*Sort Key*
* We can have either simple or composite PK.
* Composite is going to be a combination of: Partition Key and Sort Key. For all the values which have the same key, they would be sorted on the basis of sort key.
* E-commerce app example: get user order for a time range. order_id would be time sortable uuid and will be the sort key.
* Partition key always needs to be exact match. You can do range query/prefix based queries with the sort key.

*Secondary Indexes*
* It is like a read-only replica of the data. We can specify a different partition key. Eg: we want information for a specific order_id.
* Write to secondary index would be async, not blocking the write path/flow.
* Question: does RDBMS handle it in a better way by using pointers.
(35:22)

* Two type of secondary indexes:
* GSI: Writes are going to be handled in async (implemented via some stream architecture). Secondary indexes are going to be on different partitions from the main table.
    * Cassandra and MongoDB also use similar architecture. But, in case of secondary indexes, we have to do scatter gather across multiple partitions.
    * Secondary index would have a larger lag than a read replica. Could be 10-100 ms.
    * Asyn arch. helps with improving both latency and availability. Edge case to availability: if the replication log gets way too long (> threshold), secondary index can start rejecting writes on the main table.
    * Direct cost impact and *write amplification* with new secondary indexes.

46:29
**How does DynamoDB handle the problem of hot partition?**
* *Partit*
    * DynamoDB is more consistent and predictable. We get more binary responses. We won't have the performance tail off due to hot partition.
    * Partition will be colocated on storage nodes with many other partitions. We need to avoid the noise neighbour issue (?)
    * On an individual partition, we cannot exceed 3k RCU/s (read capacity unit ==> 4kB of data read) or 1k WCU/s (1 WCU ==> 1kB written).
    * They have done improvisations on that. Eg: Managing partitions by splitting them.

**Concurrent Updates in DynamoDB**
* Dynamo paper mentions maintaining multiple versions of the same key. It leaves the job on conflict resolution to the application layer.
    * *Write consistency:* All writes go to the same leader. No write consistency issues. With Cassandra, we can have write consistency issues (if we use lightweight transactions, could be resolved but would be much slower).
    * *Read consistency:* Inconsistency can be there if we hit the GSI/read replica.
    * If we have concurrent requests for key K, those would be ordered as per the arrival order.
* *Asserting conditions*: Add balance to Y account only if the balance has already been removed from X account.

**What happens when the leader goes down?**
* A new leader election will happen. That leader will ensure that is caught up with all the latest changes.
* Slight availability blip is still possible during leader election. But Amazon has high enough availability (even though leaderless would have higher availability).
* DynamoDB has added another feature to the leader election to ensure that leader election is not very frequent. If leader doesn't get the reply from the leader, before asking for starting the leader election, it asks other replicas.

**CAP Theorem**
* When we have a distributed system with replication, we could have a n/w partition b/w those nodes. In that case, we have to choose b/w one of the 2 options, we cannot get both:
    * we want a consistent view of the database.
    * our nodes won't able to able to accept reads and writes.
* DynamoDB is a CP system. In case of n/w partitions, it will reject writes. Cassandra and Dynamo are AP systems.
* It still has high availability. Its availability is better than many AP systems. One of the reason is the small size of the storage nodes (small partitions) which helps in recovering quickly. In a small storage node, we can spin up a new node quickly and copy the data.

**PACELC Theorem**
* PACELC theorem is a generalization of CAP theorem as it talks about both network partition and the normal case. If Partition, you get either one of Availability or Consistency else you get either one of Latency or Consistency.
* In the normal case, DynamoDB favor latency as it would accept writes for a quorum and not require successful writes from all nodes. 

**Transaction Support In DynamoDB**
* Transaction support in DynamoDB is very different from relational databases. 
* In case of RDBMS, transaction could be locking the rows for much longer. We could accepting user input or doing API calls in between.
* DynamoDB instead supports transactions via batch support. Long running transactions are not supported. All the instructions in the batch will be performed in a transaction providing rollback capabilities.
* Transactions are not recommended for high contention writes. It will lead to the txns failing if the write to the same item arrives at the same time.

**DynamoDB And Change Data Capture**
* Every time a write record comes into the table, it will also write that to a stream. The stream can be consumed like a Kafka or Kinesis stream for usecases like:
    * DB aggregations (on any of DynamoDB or other tables).
    * Broadcast event for other use cases: could use event bridge/SNS/Kafka for that.
    * Analytics.
* Each partition will have a different consumer.