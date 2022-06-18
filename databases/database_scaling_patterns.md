https://www.freecodecamp.org/news/understanding-database-scaling-patterns/

Example: Ride sharing app.

**Pattern1: Query Optimization & Connection Pool Implementation**
* We can cache frequently used non-dynamic data like booking history, payment history, user profile, etc. but we can't cache dynamic data like user's location or nearest cabs.
* *Adding Redundancy* 
    * We identify that our DB is heavily normalized, so we introduce some redundant columns.
    * These columns appear frequently in WHERE or JOIN ON clause in queries.
    * This reduces join queries, breaks a big query into multiple smaller queries and adds their results up in the application layer.

* *Parallel Optimization: Connection Pooling*
    * We can use connection pool libraries to cache database connections or can configure connection pool size in the DBMS itself.
    * Creating a network connection is costly, since it requires some back and forth communication between client and server.
    * Pooling connection helps to optimize on the no. of connections.
    * Connection pool libraries help to multiplex connections - multiple application threads can use the same database connection.

**Pattern2: Vertical Scaling or Scale Up**
* Upgrading RAM(eg. 2 times) and disk space(eg. 3 times).

* *How to set up machine for vertical scaling?*
    * We need to allocate a bigger machine.
    * One approach is not to migrate data from old machine rather set new machine as replica to the existing machine(primary) - make a temporary primary replica connection.
    * Once the replication is done, promote the new machine to primary and take the older machine offline. 

**Pattern3: Command Query Responsibility Segregation**
* In most of the cases, any company needs transactional capabilities on write but not on read operations.