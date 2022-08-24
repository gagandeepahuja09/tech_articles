**A Brief History of Databases**
* 1970s to 2000s ==> relational databases were made with an assumption to run on a single machine.
    * Scalability and availability both suffer.
* We needed a cluster of database nodes.
* Google BigTable, HDFS, Cassandra
* The problem with them still was a lack of joins, transactions or limitations in indexing.
* The legacy SQL database came up with features to reduce the pain of scaling out.
    * We can shard but that is generally a lot of extra work and it also comes with a lot of compromises.
* The NoSQL databases are trying to add the missing NoSQL functionality.
* While Distributed SQL databases are trying to solve both problems together from the ground up.
* Links:
    * https://www.seas.upenn.edu/~zives/03f/cis550/codd.pdf
    * https://cockroachlabs.atlassian.net/wiki/spaces/CRDB/pages/73204033/Contributing+to+CockroachDB
    * http://openproceedings.org/2013/conf/edbt/Mohan13.pdf

**Distributed SQL**
1. Distributed
2. Consistency

**Database Terms**
* *Consistency*: 
    * The requirement that a transaction must change affected data only in allowed ways.
    * CockroachDB uses both ACID, CAP consistency in less-formal definition.
* *Isolation*: 
    * CockroachDB uses the SERIALIZABLE (highest possible) isolation level.
* *Consensus*:
    * Reaching agreement on whether a transaction is committed or aborted.
    * https://thesecretlivesofdata.com/
    * Like Cassandra, CockroachDB also uses quorums.
    * When a write does not acheive consensus, forward progess halts to maintain consistency with the cluster.
* *Replication*:
    * Writes should propagate to a quorum of copies before being considered committed.
* *Multi-active Availability*:
    * A consensus based notion of high availability that lets each node in the cluster handle reads and writes for a *subset of stored data (on a per-range basis)*.
    * *Active-passive*: Active nodes receive 100% of the requests.
    * *Active-active*: All nodes receive requests but cannot guarantee that they are both up-to-date and fast.

**Architecture Terms**
* *Cluster*: 
    * A group of interconnected storage nodes that collaboratively organize *transactions*, *fault tolerance*, and *data rebalancing*.
* *Range*: 
    * CockroachDB stores all user data (tables, indexes, etc) and almost all system data in a sorted map of key-value pairs.
    * This keyspace is divided into continuous chunks called ranges, such that every key is found in one range.
    * The table is sorted by the primary key.
    * As soon as the size of a range reaches 512 MB (default), it is split into 2 ranges.
* *Replica*:
    * By default there are 3 replicas of each range on different nodes.
* *Lease-holder*:
    * The replica that holds the "lease range".
    * It receives and coordinates all read and write queries for the range.
    * For most types of tables & queries, the lease holder is the only replica that can serve consistent reads (latest data).

**Overview**
* Due to the *symmetrical behaviour* of all nodes in the cluster, SQL requests *can be sent to any node* which makes it easier to integrate with *load balancers*.

**Column Families**
* They are a group of columns that are stored together as a single key-value pair.
* The reduce the no. of keys, resulting in improved performance during writes.