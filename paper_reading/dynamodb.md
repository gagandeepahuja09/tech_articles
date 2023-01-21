**DynamoDB**
* Key properties: 
    1. consistent performance at any scale
    2. availability
    3. durability
    4. Fully managed and serverless experience
* Consistent performance at any scale is more important than median service request times. We need to optimize for the worst case in order to improve the customer experience.
* Goal of DynamoDB design: complete all requests with low single-digit millisecond latencies.

* **Fundamental Properties**
1. *Fully Managed Service*
    * Users need not worry about where their data is stored or how it is managed.
    * Frees devs from: patching software, managing h/w, configuring a distributed DB cluster, managing ongoing cluster operations.
    * Few of the automated tasks: resource provisioning, automatic recovery from failures, data encryption, software upgrades, data backups.

2. *Multi-tenant Architecture*
    * Data from different customers is stored on the same physical machine in order to ensure efficient utilization of resources.
    * Cost efficient for the customer.
    * In order to ensure that one customer doesn't affect the performance/availability of others, they have: resource reservation, usage monitoring.

3. *Boundless Scale For Tables*
    * Tables grow elastically to meet the demands of the customers. Data could be stored in thousand of servers.

4. *Predictable Performance*
    * Even as data size grows from a few MBs to 100s of TBs, latencies remain stable due to the *distributed nature of data placement*, *request routing algorithms*, *automatic data partitioning*.
    * If app is running in same AWS region as its data, we can see avg latencies of single digit ms for a 1 KB item.

5. *Highly Available*
    * Automatic replication of multiple datacenters (Availability Zones).
    * Automatic re-replication in case of disk or node failures.
    * *Global tables*: They are geo-replicated across selected Regions. Geo-replication has 2 key advantages: *disaster recovery*, *low latency access across multiple regions*.
    * *Availability SLA*: 99.99 for regular tables and 99.9999 for global tables.

6. *Flexible Use Cases*
    * Doesn't force devs into a particular *data or consitency model*.
    * Key-value or document data model.
    * During reads, devs have the flexibility of choosing *strong vs eventual consistency*.

* Key Aspect: *Providing a single-tenant experience to every customer using a mult-tenant architecture*.

* **Lessons Learnt**
* In order to improve the customer experience, they *reshape the physical partitioning scheme of the tables, depending on the customer's traffic patterns*.
* In order to protect against hardware failures (Durability) and software bugs, they perform continuous verification of data at rest.
* In order to maintain high available and safely add new features requires:
    * Careful operation discipline and tooling.
    * Formal proofs of complex algorithms.
    * Game days (chaos and load tests).
    * Upgrade / downgrade tests.
    * Deployment safety.
* *Designing systems for predictability over absolute effeciency improves system stability*. While components like caches can improve performance, *do not allow them to hide that would be performed in their absence, ensure that the system is always provisioned to handle the unexpected*.

**2. History**
* Lesson learnt from Dynamo: It was providing application direct access to database instances. This led to facing *scaling bottlenecks* like:
    1. Connection management.
    2. Interference b/w concurrent workloads.
    3. Operational problems with tasks like schema upgrades.
* Problem solved by adopting a *service-oriented architecture*.
* *Operational complexity*:
    * Teams had to take care of their own installation and upgrades.
    * Teams had to become expert on various parts of the DB service.
* S3 and SimpleDB were released during similar time to provide managed and elastic experience and reduce operational burden.
* Amazon teams preferred using these 2 over Dynamo even if Dynamo was more suitable for their use case because of ease of use.
* *SimpleDB*
    * Fully-managed elastic NoSQL database.
    * Limitations: 
        * limited storage (10 GB per table) and request throughput.
        * devs had to divide data b/w multiple tables to satisfy their requirement.
        * unpredictable read and write latencies since all attributes were indexed and the index had to be updated with every write.
* Best solution: combine best of Dyanamo (incremental scalability and predictable high performance) and SimpleDB (ease of administration of a cloud service, consistency, and a table based data model that is richer than a pure key-value store).

**3. Architecture**
* DynamoDB table -> collection of items -> collection of attributes.
* Each item is uniquely identified by a primary key. Schema of primary key is defined during table creation.
* It contains a partition key or a partition key and a sort key (a composite primary key).
* A partition key's value is hashed and its output determines where the item will be stored.
* Multiple items can have the same partition key in case of a composite PK but they should different sort keys.
* Secondary indexes are also supported.
* Supported operations: PutItem, GetItem, UpdateItem, DeleteItem.
* (How?) DynamoDB supports ACID transactions, enabling applications to update *multiple items*(?) without compromising the *scalability, availability and performance characteristics* of DynamoDB table.
* In order to handle the *throughput and storage requirements* of the table, a DynamoDB table is divided into *multiple partitions*.
* Each partition hosts a disjoint and contiguous part of table's key range.
* Each partition has multiple replicas distributed across different AZs for high availability and durability.
* *Replica group*: The replicas for a partition form a replica group.
* Multi-Paxos used by replicas for leader election and consensus.
    * Any replica can trigger a round of the election.
    * Once elected, a replica can maintain leadership as long as it periodically renews its leadership lease.
* Only the leader replica can serve *write and strongly consistent read requests*.
* *Write path*: 
    * Leader for the replication for the key being written generates a WAL record and sends it to its peers.
    * Write is acknowledged to the application once a quorum of peers persists the log record to their local write-ahead logs.
* If the leader of the group is failure detected (considered unhealthy or unavailable) by any of its peers, the peer can propose a new round of election to elect itself as the new leader.
    * The new leader won't serve any writes or consistent reads until the previous leader's lease expires (question: won't that make the service unavailable for that specific key for that duration? can we expire the prev leader's lease after leader election completion?)
* Storage nodes contain both the write ahead logs and the B-tree.
* In order to improve availability and durability, we can have *log nodes* that only store WALs.
* DynamoDB consists of tens of microservices.
* Core services:
    * *Metadata service*: It stores the routing information about the tables, indexes and the replica groups.
    * *Request routing service*: 
        * Responsible for authenticating, authorizing each request to the appropriate server. The request routers look up the routing information from the metadata service.
        * All resource creation, updation, and data definition requests are routed to the autoadmin service.
    * *Storage service*: for storing on storage nodes.
    * *Autoadmin service*:
        * It is like the CNS of DynamoDB.
        * It is responsible for *fleet health*, *partition health*, *scaling of tables*, and *execution of all control plane requests*.
        * It continuously monitors the health of all the *partitions* and replaces any replica deemed unhealthy (slow or unresponsive or being hosted on bad hardware).
        * It also performs health checks of all core components of DynamoDB and replaces any hardware that is failing or has failed.
* Other services support features like: 
    * Point-in-time restores
    * On-demand backups
    * Update streams
    * Global admission control
    * Global tables
    * Global secondary indexes
    * Transactions

**4 Journey from provisioned to on-demand**
* Partitions are a way to *dynamically scale both the capacity and performance of tables*.
* In the original release, customers explicitly specified the *provisioned throughput* in terms of RCUs (read capacity units) and WCUs (write capacity units).
* For items upto 4KB in size, 1 RCU can perform 1 strongly consistent read request per second.
* For items upto 1 KB in size, 1 WCU can perform 1 standard write request per second.
* In order to scale the table elastically, partitions could be split and migrated.
* Early version of dynamoDB tightly coupled the assignment of capacity and performance to individual partitions which led to challenges.