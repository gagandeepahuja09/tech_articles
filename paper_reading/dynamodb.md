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