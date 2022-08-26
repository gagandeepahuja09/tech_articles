* https://www.cockroachlabs.com/blog/how-we-built-cockroachdb-serverless/
* When creating a server, we have to estimate on the no. of servers. Both too low and too high are a problem.
* Serverless means that we have outsourced the problem.
    * CRDB will do all the work of allocating, configuring and maintaining the servers.
    * We only pay for what we actually use, without needing to figure out upfront what that might be.

* *CRDB Serverless Architecture*
    * Hosting 1000s of virtualized CockroachDB clusters on a single underlying physical CockroachDB database cluster.

**Single-Tenant Architecture**
* A single physical CockroachDB cluster was intended for dedicated use by a single user or organization. Multi-tenancy enables a single physical CockroachDB cluster to shared by multiple users or organizations.
* Multi-tenant concept is similar to virtual machines. Each tenant get its own virtualized CockroachDB cluster that is hosted on the same physical CRDB cluster and yet is secured and isolated from other tenant's clusters.
* SQL --> KV Layer --> This can fan-out to other nodes.

**Multi-Tenant Architecture**
* Each tenant should be isolated from other tenants in terms of *performance and security*.
* If we share the SQL layer across tenants, one tenant's SQL query could disrupt the performance of other tenants in the same process.
* Sharing the same process could also introduce many cross-tenant security threats.
* If we give each tenant its own set of isolated processes, we loose out on one of the major benefits of a multi-tenant architecture: the ability to effeciently pack together the data of many tiny tenants in a shared storage layer.
* Solution: SQL Layer and 2 of the KV layers: Transaction, Distribution are isolated while Storage & Replication layer are shared.

* Each tenant receives an isolated, protected portion of the KV keyspace.
    * Rather than generating a key like `/<table-id>/<index-id>/key`, SQL will generate a key like `/<tenant-id>/<table-id>/<index-id>/key`.
    * The storage nodes authenticate all communication from the SQL nodes and ensure that each tenant can touch only that are prefixed by its own tenant identifier.
    * In order to ensure that a single tenant cannot monopolize resources on a single tenant, we measure the no. and size of read and write requests coming from each tenant and throttle its activity if it exceeds some threshold.

**Serverless Architecture**
* It uses K8s to operate serverless clusters, including both shared storage nodes and per tenant SQL nodes.
* Each node runs in its own K8s pod which is 