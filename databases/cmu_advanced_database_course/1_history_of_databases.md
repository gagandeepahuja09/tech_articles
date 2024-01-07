https://www.youtube.com/playlist?list=PLSE8ODhjZXjasmrEd2_Yi1deeE360zv5O

* A lot of issues that the databases were facing in the 1960s and 70s are still relevant today.
    * How to run transactions correctly.
    * How to maintain indexes.
* *History repeats itself.*
* SQL vs NoSQL database debate is reminiscent of Relational vs CODASYL (Network data model).
    * Spoiler: Relational model almost always wins.
* The only exception could be machine learning.

# 1960s
* *Network data model (GE: IDS)*
* Tuple-at-a-time queries.
* We need to apply nested for loops to find the parent and the child.
    * Complex queries: low-level for loops.
    * Membership sets can easily get corrupted.
* Supplier -> supplies (2 columns: parent, chield) -> supply -> supplied_by (parent, chield) -> price.

* *Hierarchical (IBM: IMS: Information Management System )*
    * Still in use. Many ATMs still use this.
    * Programmer defined physical storage format.
        * We could define the data structure that we would want to preserve the data on disk. Some sort of hash table or order preserving tree.
    * Tuple-at-a-time queries.
* Problems
    * Duplicate data.
    * No independence
        * Earlier I used hash table but later I realize I need range queries. I have to dump all the data and load it as B+ tree.

# 1970s - Relational Model
* Seeing the problems of developers rewriting programs every time the schema or layout changes, Ted Codd from IBM came up with relational model:
    * Store data in simple data structures.
    * Access data through high-level language. (QL => SQL)
        * Back then, these ideas seemed controversial. C => high-level language. People though that should be written in assembly language.
    * Physical storage left upto implementation.
* *Instead of tuple at a time, apply hash-joins.*

# 1980s - Object Oriented Databases
* These databases tried to solve the problem of taking objects which could potentially be nested array and break them up into records or tuples.
* They tried to store the objects directly.
* While the databases are still not around, many of the technologies are still in use. eg. storing JSON columns.
* Problems:
    * Queries become more complex when everything is stored in JSON.
    * Unlike SQL, no standard API. (MongoDB, Redis are the standards.)

# 2000s - Internet Boom
* SQLite: early 2000s.
* All the big players were heavy weight and expensive.
* Open source database were missing important features.
* Many companies wrote their own custom middleware to shard out and scale database across single-node database instances.
    * More reads and writes.

# 2000s - Data Warehouses
* OLAP DBMS
    * Distributed, shared-nothing.
    * Relational, SQL
* Columnar data storage.

# 2000s - NoSQL
* Focus on high-scalability and high-availability
    * Compromise on ACID.
    * Schemaless
    * No relational model.
    * Custom APIs instead of SQL.

# 2010s - NewSQL
* Provide same performance for OLTP workloads as NoSQL DBMS without giving up ACID.

# 2010s - HTAP
* Execute fast OLTP like NewSQL while also executing complex queries like a data warehouse system.

# 2010s - Cloud System
* First DBaaS offerings were containerized versions of existing databases.
* There are also DBs built from scratch specifically for running in the cloud environment.

# 2010s - Shared-disk Engines -- Data Lakes
* Instead of writing to local disk, the DBMS writes to HDFS like S3.
* This allows independent scaling of stage and compute.
* Since the data is writing in append-only mode, if favours log-structure storage approach. 

# 2010s - Graph Databases
* Graph-centric query API.
* Recent research demonstrates that it is unclear whether they provide any additional advantage.

# 2010s - Timeseries Databases

# 2010s - Specialize Systems
* Embedded, Blockcain,etc DBMSs 