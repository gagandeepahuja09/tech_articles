* Transactions provide an *illusion* that a group of operations that modify some data have *exclusive access* to it and either *all* operations execute successfully or *none* does.
* Transactions that update data owned by multiple services are challenging to implement.

**Concurrency Control**
* Optimistic concurrency control doesn't block. It checks for conflicts only at the very end of the transactions.

**Log Based Transactions: Why Dual Writes Are Bad?**
* https://www.confluent.io/blog/using-logs-to-build-a-solid-data-infrastructure-or-why-dual-writes-are-a-bad-idea/
* Consider examples where we need to ensure writes to multiple datastores like MySQL, ES, Redis.
* Option 1: Dual writes: problem: inconsistency. (11_dual_writes_problem).
    * As can be seen from the example, the two datastores will permanently remain inconsistent until sometime later someone comes and overwrites X again.

*Solution: Do all your writes in a fixed order, and store them in that fixed order.*

* Key points:
    * If we do all our writes sequentially, without any concurrency, then we have removed the potential for race conditions.
    * If we write down the order in which we make our writes, it becomes easier to recover from partial failures.
* Whenever anyone wants to write some data, we append that write to the end of a sequence of records. That sequence is *totally ordered, append-only and persistent*. We will such data structures as simply *log*.

**Logs Are Everywhere**
1. DB storage engines
2. DB replication
3. Distributed Consensus
4. Kafka

**DB Storage Engines**
* In B-trees, if there is not enough space in the page that we are inserting, we need to split it into 2 separate pages.
* Now, when we are writing, we need to write at least three pages to disk: the two pages that are a result of the split and the parent page. These pages may be stored at different locations on disk.
* If a DB crashes happens mid-way, we might be in a state where some pages have the old data while others have the new data. We could also end up with dangling pointers.
* Databases solve this problem with WAL. Only after a record has been written in WAL, can a B-tree be modified.

**DB Replication**
* How does the data get replicated to the follower? They use a replication log which may be same as the WAL (like Postgres) or a separate replication log file (like MySQL).
* How do we handle inconsistencies in case of network partition?
    * The log has a very nice property, because only the lead ever appends to it, we can give a sequence number. When we know a follower's current number, we know that all the records prior to that have been successfully processed.
    * Whenever the follower recovers, it asks the replication logs from a certain offset.

**Distributed Consensus**
* A client proposes a value, example X = 8 (which may mean that node X is the leader of partition 8), by sending it to one of the Raft nodes. That node collects values from other nodes. If a majority of nodes agree that value should be X = 8, the first node is allowed to commit the value.
* Raft also builds up a log of the values that have been agree upon over time.

**Kafka**
* The interesting thing about Kafka is that it doesn't hide the log from us.
* It exposes it to us, so that we can build applications around it.