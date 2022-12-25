* Storage: could be stored in RAM/disk/SSD/blob storage. All of the writes and read speed and cost per data units. 
* Tiered-storage: A single application being able to use different type of storage in a configurable manner. (4:58)

* **Cost, Performance and Flexibility**

* Coupled and De-coupled systems.
* Coupled: Storage tightly coupled with the compute. (Analytics)
* De-couple systems: Storage is not decouple to the compute.  Presto is an example of that. We use some cheap object store like S3 to keep the data. We don't have POSIX APIs and need to make a network call. Latencies will have to be in seconds. The cost is better but it takes a hit on performance.

15:00.
* Common solution to this problem used to be: make use of both systems. Keep the recent data in tightly coupled system, keep the historic data in decoupled system. We need to maintain multiple systems and need to have a federation layer which decides where to send the query.
    * Lack of configurability and the migration not being straightforward. We need to involve data ingestion pipelines.
* Tiered storage will help to choose the tradeoff in all 3 aspects. 