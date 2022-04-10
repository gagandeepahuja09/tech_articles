Fully Managed: Many of the NoSQL solutions and new solutions are fully managed which frees up the developer from handling administrative tasks like: provisioning, replication, auto scaling, back-ups, multi-region support out of the box.

Distributed: Spread across multiple nodes(replicas).

Highly Available: The distributed nature of DynamoDB, helps with scenarios when one of the replica goes down.

Unlimited scalability: Via auto scaling.

Document Store: Lets us store unstructured JSON documents with a dynamic schema. It does enfore data types but every document need not conform to it.

***********************************************************************************

Partitions
* Partitions in DynamoDB are spread across replicas.
* Create a new table in DynamoDB creates a single partition.
* Each partition can hold upto 10GB of data and can handle 3k RCU & 1k WCU.
* 1 RCU => 1 Strongly consistent read or 2 Eventually consistent reads per second for document of size 4kB.
* The no. of partitions increases when RCUs or WCUs increase beyond a certain threshold or the data growth of a partition goes beyond 10GB. ==> Auto Scaling

***********************************************************************************

Consistent Hashing
* Without consistent hashing, when the no. of partitions change, we need to reshuffle which leads to a lot of network bandwidth utilization in data movement.
* When we add a new replica, only the keys b/w the new replica and the replica to its right need to be remapped and redistributed which leads to minimal data movement.

***********************************************************************************

Primary Lookups: Partition key + optional sort key

Partition Key
* For selecting the partition to which document belongs.
* Parition key is passed through an MD5 hash function.
* The mapping of which partition resides in which replica is part of partition metadata system.
* That way partition key helps to decide both the partition and the replica where the document resides.
* As long as the cardinality of the partition key is high, the document will be evenly distributed across the replicas without creating hot spots.
* Example of a good partition key: UUID. Bad partition key: enums.

* If a table is created using the partition key alone, then DynamoDB allows accessing individual documents by its partition key.

* If a table is created using the partition key and sort key, then DynamoDB allows two access patterns:
    1. Access individual components by its partition key and sort key.
    2. Access all documents for a given partition keys.


Sort Key
* Ensures that for a particular partition key, the results are sorted by the sort key.
* Helps in range queries, both of filter and sort by type.
* Eg. user transactions table => user -> partition key, transaction time -> sort key.

***********************************************************************************

Replication
* Every partition is replicated across 3 servers(replication factor = 3) to provide fault tolerance. 
* Out of which 1 replica is the leader(writes). 1 sync follower and the other is async follower.
* Leader + 1 sync done => Write considered successful.
* DynamoDB also ensures the placement of replicas of each partition into multiple availability zones to prevent data loss due to the unavailability of a particular availability zone.

***********************************************************************************

Indexes
* Traditionally indexes are an additional data structure and are used for efficient queries. They act as signpost for original table.

* In DynamoDB, an index is a completely different table and can include the same or different partition key or sort key.

* It can also optionally copy a subset of attributes of the primary table. They have exact same replication factor.

* It supports upto 5 different LSI & GSI per table.

LSI: Local Secondary Index
* Has the same partition key as the main table but optionally it can include a sort key different from the main table.
* Since the partition key for both the main table & index table are the same, both the partitions reside on the same physical server.
* This allows them to support strong consistent reads.

GSI: Global Secondary Index
* Can have different partition key, sort key from the main table. 
* Main table and index table may or may not reside in the same physical server(partition) as the partition key is different. 
* It only supports strong consistent reads.
* Both LSI, GSI can optionally has a subset of attributes from main table.

***********************************************************************************

Data Structure
* Each partition primarily uses 2 data structures: B-Tree & replication log.
* The partitions are stored on solid state drive(SSD) on disk in each partition.

***********************************************************************************

B-Tree
* Most suited for on-disk data structures due to its lower height and high fanout per level.
* If DynamoDB is created with partition key alone, then the partition includes one B-tree per partition.
* If created with partition key and sort key, the the partion key includes a B-tree which is a composite index of (Partition Key, Sort Key) allowing both point in time lookup by (Partition, Sort Key) and range lookup by Partition key.  

***********************************************************************************

Replication Log
* It serves as a relayer on followers and indexes.

***********************************************************************************

Membership
* Leader periodically sends heartbeats to its followers to keep its leadership active.
* If any of the followers don't receive a ping for more than a specified interval, they consider the leader dead and initiate a leader election to elect a new leader.
* It employs the distributed consensus algorithm Paxos for leader election.
* Paxos is a 2 step process for Propose votes and Commit for electing a new leader.

***********************************************************************************

Architecture

Diagram: https://docs.google.com/document/d/17uiIuwqJtc6HiBPgr3ZLHFU5NyEqcnV_Bth1WSmA5PE/edit

Example:
Partition Key: transaction_id
LSI Partition Key: transaction_id
LSI Sort Key: timestamp
GSI Partition Key: user_id
GSI Sort Key: timestamp

* GetItem & PutItem

*** PutItem ***

Request Router
* The write request first hits the request router module.
* The request router module resides in a separate availability zone from the storage node.
* Every availability zone hosts multiple request router modules.
* It performs Authentication & authorization and then computes the MD5 hash out of the partition key to identify the partition to which the document belongs.

Partition Metadata System
* The request router enquires partition metadata system to identify the replicas hosting the partition and also the replica hosting the leader partition.

B-tree & Replication log
* Once the write request is persisted to the leader partition, it's first persisted locally to B-tree and then appended on replication log. Both these operations happen atomically.

Leader to Sync Follower to LSI(if present)
* Similar B-tree & replication log operation.
* The operation is performed for both the LSI and the sync follower of the LSI.
* After persiting in leader + sync follower + LSI + sync follower of LSI the request is considered durable and a success report is sent to the client.

Log Propagator
* Log propagator reads the replication log and propagates the changes across other replicas(async followers, LSI, GSI in the same order).
* Since some of these changes are applied async, there are 2 modes of document access: Eventually consistent and Strongly consistent.


*** GetItem ***

* The read request for both the main table and the index tables works in a similar fashion.
* Includes following parameters: Table name(Main/LSI/GSI), Partition Key, optionally a sort key and/or consistency level.
* Request first hits the request router => Authentication & authorization => MD5 hash of partition key to find the partition => Partition metadata system to identify all the replicas holding the partition.
* Eventually consistent => Forwarded to any of the 3 partitions.
* Strongly consistent => Forwarded to leader or sync follower.

***********************************************************************************

Auto Admin(DBA of DynamoDB): Core responsibilities
    1. Auto Scaling
    2. Provisioning
    3. Failover
    4. Replacement of replicas

***********************************************************************************

Table Provisioning
* DynamoDB operates on pay for throughput rather than pay for storage.
* DynamoDB mandates specifying RCU & WCU while creating the table.
* If these capacities are breached, further requests will be throttled.
* The provisioning of the RCUs, WCUs for partitions is done in equal distribution wrt the table. Eg. RCU for table = X and 3 partition => RCU for each partition => X / 3.
* This means that requests will still get throttled, even if they receive unequal distribution and other partitions are under-utilized.
* Hence it's very important to choose a partition key such that it evenly distributes the traffic across the partitions and has a high cardinality. Good PK: UUID, Bad PK: status fields like enums.

***********************************************************************************

Rate Limiting
* DynamoDB uses leaky bucket algorithm for rate limiting.
* It creates a leaky bucket per partition.
* Buckets are refilled every second with appropriate tokens matching RCU/WCU per partiton.
* For every read/write request tokens are removed & if the bucket is empty within a second, it throws a ProvisionedThroughputExceeded exception.
* DynamoDB has built multiple solutions to let applications continue running without throughput exceeded exception.

***********************************************************************************

Burst Capacity
* Built to support spiky patterns at certain intervals.
* If a partition's provisioned capacity is unused for read / write requests, DynamoDB reserves a portion of that unused capacity for 5 minutes and are utilized during bursts when the threshold is exceeded.

***********************************************************************************

Adaptive Capacity
* This was introduced to let applications with imbalanced load run indefinitely.
* DynamoDB increases the throughput of hotspot partitions by a factor called adaptive rate using a feedback mechanism dictated by the PID controller.

Hotspot Documents: If few documents are continuously hit for read and write requests in a given partition, adaptive capacity balances these partitions such that they don't reside in the same partition thereby preventing throttling.

***********************************************************************************

Auto Scaling(All this would have to be done manually in MySQL databases)

* If the RCU per partition threshold (3000 / No_of_partitions) or WCU per partition threshold (3000 / No_of_partitions) or the data growth of the partition exceeds 10GB, auto admin initiates new partition creation and migrates half of the data from old partition to the new partition.
* Consistent hashing => minimal data movement and consumption of bandwidth.
* Partition metadata system is updated with the latest information on partition and replica mapping. 

***********************************************************************************

Backups And Restore

Backup
* Replication log in every partition is batched together and uploaded to S3 at regular intervals.
* B-tree in each partition is scanned and a snapshot is taken periodically into S3 at slightly higher intervals.
* Once the snapshot is taken, R Log & previous snapshot can be truncated from S3.

Restore
* The restore operation will scan every partition backup on S3 and look for the latest partition before the given time frame and use replication log to replay remaining events post the snapshot. ==> On-demand backup

Point in Time Recovery
* Provides data backup every second so that we can recover to any given second in the last 35 days.
* Snapshot, R Log can't be deleted for 35 days. ==> extra charge.