**Dissecting Github Outage - How databases are managed in production**
* The DB team rolled out an upgraded version of ProxySQL.

**What is ProxySQL**
* It sits as a proxy between the servers/clients and the MySQL cluster.
* Every connection goes through ProxySQL.

**Why do we need ProxySQL in production?**
* *Better connection handling* 
    * Connection pool
    * Connection multiplexing

    * If each API server is making connections with the MySQL cluster, it will add unnecessary load on the MySQL cluster. 
    * MySQL cluster has a theoretical limit on the number of connection that it can handle. ProxySQL ensures that this limit is never breached.

* *Gatekeeper to enhance security and routing*
    * Route writes to primary and route reads to replicas.
    * Insteading of API servers requiring to keep this logic, ProxySQL does this seamlessly.
    * We can configure rules and fire query. ProxySQL will automatically route the request to correct and intended node.

* *Caching*
    * Given that ProxySQL is transparently sitting between servers and the database, it is the best place to cache common query responses for certain use-cases for a ttl.

* *Temporary access management*
    * We won't want to give access to DB credentials to many folks in the organization.
    * TAM can help with creating temporary users in DB and deleting them after a few hours.

**What failed?**
* After a week, the primary node crashed.
* "Orchestrator" detected the failure and quickly promoted a replica to the new master.
* The newly promoted master also failed. (probably because it also wasn't able to handle the load). This looks like a classic case of cascading failure.