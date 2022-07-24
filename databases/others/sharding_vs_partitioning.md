Sharding: Method of distributing data across *multiple machines*.
    * Shards are physical servers.
Partitioning: Splitting data within the same instance.

*How a database is scaled?*
* A database server is just a DB process (mysqld, mongod) running on an EC2 machine.
* On an EC2 server, we install a MySQL server and start the process. That process exposes a port.
* The MySQL DB uses the local disk of the virtual server (EC2 instance).

* *Vertical scaling*: 
    * Giving our CPU instance more CPU, RAM and disk.
    * There is a limit beyond which we cannot scale vertically due to hardware limitations.

* Large no. of reads
    * Read replica.

* Each database server is sharded while the data is partitioned.
* Consider that there are 10 partitions of the data. These partition can reside in same or different database servers.
* *Load balancing across partitions*: If we observe that some partitions of the shard are getting hot due to large no. of requests, we can move few few of its partitions to another shard.

* *Read Replica*: Classic case of sharding but no partitioning as both shards have exactly the same data.

* *Advantages of sharding*
    * Handle large reads and writes
    * Increase overall storage capacity
    * Higher availability

* *Disadvantages of sharding*
    * Operationally expensive and complex. Ensuring replication lag is at bare minimum.
    * Cross-shard queries are expensive.