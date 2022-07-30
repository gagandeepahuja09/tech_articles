Video: https://www.youtube.com/watch?v=1NuvxQEoVHU&ab_channel=TheGeekNarrator

* BigTable by Google was the advent of NoSQL by taking off the the primitives of refrential integrity.

**Problem with traditional RDMBS**
* These databases were designed for a single server.
* Horizontal scaling adds complexity (diff to maintain).
* Operational overhead due to active-passive systems.
* Distribution is about being distributed at all levels of the stack.
* Distributing database is not just about sharding. It is about distributing consensus, execution.

**Three Layers of a DB**
1. Language Layer: SQL generally rules the world.
2. Storage Layer
3. *Distributed Execution Layer (Middle Layer)*
    * Moving from active-passive to active-active.
    * Every single node acts as an endpoint and can be used. This is what is required for truly distributed systems (supporting distributed concepts natively).
    * This takes away all the complexities from the application developers to the DB as was the case with a single DB server.

* CockroachDB: intuition behind the name: the DB you can't kill.
* In a lot of large banks, due to security problems, after every month or two, they repave the entire machine (killing the process, OS, etc). A lot can go wrong in this process but they have no other option.

* *Spanner*: CockroachDB was inspired by the spanner white paper.
    * Strong consistency
    * Serializable isolation
    * Georeplicated data
    * Highly available and highly fault tolerant

* Storage layer
    * Distribution of data and replication of data.
* Distribute Execution layer
    * Like mapreduce.
* Language Layer
    * What are the things you need to add to SQL to make it distributed. Eg. location of the data. Making them primitives of the SQL language.

**How writes in CockroachDB work?**
* When writing data to CockroachDB, we are writing some odd number of times. (3, 5, 7, ...)
* *Distributed Consensus*: They use Raft.
* Instead of writing the data at a single place and then doing asynchronous replication, it uses quorums.
* As longs (n + 1) / 2 come back and see that the data is written, we are fine.
* Default replication factor: 3.
* Raft checks that at a give time, do I have all three copies and are all those copies synced.
* Raft also has a leader which helps to check for atomic commits.
* Note: this is not replication but multiple writes asynchronously.

**How reads work?**
* We will get the latest data while querying the raft leader but we might get stale data while querying the follower node.

**How is data modelled?**
* We convert data to KV pairs.