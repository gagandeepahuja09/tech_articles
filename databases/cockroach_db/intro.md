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

**Terms**
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
    * A consensus based notion of high availability that lets each node in the cluster handle reads and writes for a subset of stored data (on a per-range basis).
    * *Active-passive*: Active nodes receive 100% of the requests.
    * *Active-active*: All nodes receive requests but cannot guarantee that they are both up-to-date and fast.