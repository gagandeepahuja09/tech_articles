Blog: https://blog.flipkart.tech/tiered-datastore-solution-for-high-data-growth-mysql-using-distributed-sql-databases-dsql-472e391deb7

* MySQL widely used due to ACID guarantees.
* Requires the overhead of data maintainence.

Requirements
* Until entity completes it's lifecycle, it has to be in MySQL cluster as reads & writes happen very frequently.
* After lifecycle completion, uptil a certain point(eg 1-2 year) for operational uses, it has to available in a queryable format.
    * Read only.
    * Horizontal scalability and MySQL like querying ability.
* Blob storage for 5-8 years for compliance reasons.

Challenges with Sharded MySQL
* Flipkart is multi-tenant.
* Each tenant will have its own database => Compliance requirements.
* Sharding each tenant = Operational nightmare = Maintaining multiple shards per tenant.
* If we want to have only 1 shard per tenant, we'll have to constantly delete data to keep the active shard small and manageable.


Hot Store, Warm Store, Cold Store
Warm Store: 
    * We'll use Distributed SQL.
    * Using NoSQL comes with overhead of:
        * Custom data migration
        * Completeness check
        * Schema changes