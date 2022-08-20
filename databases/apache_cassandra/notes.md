<!-- Source: https://www.youtube.com/watch?v=V1EO_0i3RNA&ab_channel=TheGeekNarrator -->

**What is Apache Cassandra?**
* It is a transactional database (not analytical).
* Less number of trade-offs:
    * Scales linearly.
    * Self-healing and up-time guarantees.
    * Distributed: Multi-master, Multi-datacenter.
* Comparison b/w DynamoDB, HBase, Cassandra:
    * Difference in architecture: HBase has a master oriented architecture.
    * The *shared-nothing* architecture in Cassandra is critical. Every node is independent and coordinates with other nodes.
        * This architecture also helps with the resilience, up-time and partition tolerance.
    * DynamoDB and HBase have some form of SPOF.

**What is a shared nothing architecture?**
* In a distributed system, there are mainly 3 resources: compute, network and storage.
* It is shared nothing but coordinated.
* When a new node is added, it is given a seed node (the ip address of one of the running nodes in the cluster) and from that they discover the rest of the cluster.
* It doesn't heavy coordination like ACID. eg: for a cluster containing 1000 nodes, it need not get a confirmation from all before committing. It only has to coordinate with a subset of the nodes.

**How writes work in Cassandra?**
* Like DynamoDB, the distribution of the data is based on the concept of partition key.
* We can think of Cassandra as a distribute hash map.
* Each partition key maps to a hashmap and those hashmaps exist on individual nodes.
    Node, Start range, End range, Partition Key, Hash Value.
* The partition key goes through a distributed hash algorithm and get transformed into murmur3 hash. This gives a 64-bit number.
* Each node has 1/4th the range of all 64-bit numbers.
* Query processor.
* We get from cluster operation to node-local operation.
* It writes to the commit log first. (durable write) and then into a mem table.
* If we are talking about certain consistency levels, then it has to coordinate with other nodes alsos.
* It doesn't support random writes and does not require writing to a B-tree.
* It helps with the fast writes as the commit log is only an append only log file.
* The SSTable process will take care of flushing from Memtable to the SS-table. Once that is done, it is removed from the commit log.
* The better way to shut down the node is to flush it to disk first it dumps all the mem-table to disk and pulls out all the commit logs. This will help with not taking a long time to read the entire commit log during starting up.
* The SS-tables are indexed.

**How many copies are written on a write?**
* Keyspace: stores table (schema) and replication information (replication factor).
* It should ideally be 3. It is the right amount for protection along with note blowing out the budget.
    * This means that every table that gets created in that keyspace will have 3 replicas.
    * Each node is responsible for one quarter of the data.
* Even if the no. of nodes in the cluster is 4 or 100, they will be storing only 3 copies of the data.
* Question: if we have 1000 nodes and replication factor of 3, then how are we ensuring that every node has 1/4th of the data as it should only be 3/1000 in this scenario.

**How does the replication work?**
* Async or sync replication? Does it wait for all the replicas to have written first before commiting?
* The developer can make a choice here. The dial in this case is called consistency level.
* Strongest consistency: all 3 nodes need to agree that the data is on their disk.
    * We won't require it for almost all cases.
    * Even if one of the node goes down, we can't satisfy this consistency level.
    * Most commonly used consistency level is *quorums*. quorum = (replication_factor / 2) + 1. We need a response only from these many nodes.
    * Even if the write was not successful on some of the other nodes, it will gather the information from the other nodes where the write was successful.
    * The lowest consistency level is one node. It's rarely used. Could be used for IOT like cases.
* 3 is also the right number to start because, we require the majority in quorum. Failure domain ==> very low probability for 3 nodes to fail together.

**How do reads work? What role does consistency level play?**
* The partition key helps with going to a specific node (or its 2 replicas) out of a 1000 node cluster.
* After reaching the partition key, it uses mechanisms like bloom filter and key caches to reduce the disk seeks.
* It finds the SS table on disk. BigTable.
* The coordinator needs to match with the read done on another node. They have to match with each other by timestamp. If the other node has incorrect data, the other nodes will correct that node. That is called *Read Repair*.
* Spanner paper from Google: atomic clocks.
* There is a lot of flexibility in many of the features in Cassandra. The same is true for handling time. It could be handled both at client side and server side. Time drift among clusters is a real issue and is handled with latest version of Linux Kernel.
    (Not very clear on the time related discussion.)

**What is allow filtering and why is it not recommended**
* Cassandra uses a SQL like query language called CQL.
* Cassandra is meant for partition key based queries. That allows the coordinator to forward the query to a particular node. It is also not meant for JOIN like queries.
* When we are running a query like SELECT *, it will go through the entire cluster. Cassandra will limit the result to 1000 by default.
* In order to view more results, we can use allow filtering but it's not recommended on production.

**What is the right way to model data in Cassandra?**
* In relational model, we first design the entities and then move to the queries that we would support.
* But in Cassandra or DynamoDB, we do the reverse.
* Eventually we get to a point where we have to denormalize the tables because the joins are becoming a liability.
* Common assumption is that Cassandra doesn't give the query flexibility, agility which relational databases can offer.
* Older relational databases were built to optimize on disk space since it was expensive which isn't the case anymore.

**Modelling A Chat Application**

50:33