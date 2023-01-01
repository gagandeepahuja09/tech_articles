* Storage: could be stored in RAM/disk/SSD/blob storage. All of the writes and read speed and cost per data units. 
* Tiered-storage: A single application being able to use different type of storage in a configurable manner. (4:58)

* **Cost, Performance and Flexibility**
* Coupled and De-coupled systems.
* Coupled: Storage tightly coupled with the compute. (Analytics)
* De-couple systems: Storage is not decouple to the compute.  Presto is an example of that. We use some cheap object store like S3 to keep the data. We don't have POSIX APIs and need to make a network call. Latencies will have to be in seconds. The cost is better but it takes a hit on performance.
* Common solution to this problem used to be: make use of both systems. Keep the recent data in tightly coupled system, keep the historic data in decoupled system. We need to maintain multiple systems and need to have a federation layer which decides where to send the query.
    * Lack of configurability and the migration not being straightforward. We need to involve data ingestion pipelines.
    * This will lead to high operational maintainence overhead.
* Tiered storage will help to choose the tradeoff in all 3 aspects. 

**How to implement tiered-storage?**
* Federation layer has its own problems.
* Caching or lazy loading works well only when we are well aware of the access patterns and the data doesn't frequently update.
* Caching won't improve the worst case.
* In pinot, they kept configurations to ensure that some part of data is tightly coupled while the other is de-coupled.

**Implementation of tiered-storage in Pinot**
* Decoupling storage from compute.
* Parallelism factor of eg. 20.
* Pinot operated with an assumption that the data is present locally, hence an abstraction had to be created.
    * De-coupled systems allow the scaling of storage and compute independently.
* Each round-trip to s3 would take around 100 ms and there could be 100 different segments.
* Prefetch: Fetching during the planning phase.
* Unlike lazy loading, a columnar approach was used. Making use of the ranged-get query from S3, they were able to fetch only the portions which were actually required. Apart from that, the index was also fetched.

**What happens when we query for more number of or all columns**
* Pruning via bloom filters is done. There are also various other pruning techniques.
* Multiple stress tests were done. Observation: Bandwidth limit.