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
