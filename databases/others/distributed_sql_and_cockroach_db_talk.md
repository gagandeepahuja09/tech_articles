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