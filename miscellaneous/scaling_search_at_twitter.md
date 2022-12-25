* Advantages of ElasticSearch
    * Speed, scalability, distributed nature, Simple REST APIs.

**Standardization Requirement at Twitter**
* Earlier every team was allowed to spin-up their ES clusters.
* The team owning the cluster had the responsibility to set things up correctly.
    * Teams could be logging differently.
    * There was no throttling. A team abusing the cluster could take the entire cluster down.

**ElasticSearch Proxy**
* Proxy standardized throttling, routing, security, authentication, monitoring.
* *Monitoring* - cluster health, success rate, failure rate, latency.

**Ingestion Service**
* Rather than allowing services to directly ingest data to elasticsearch, they can write to an API which will push to the Kafka topic.
* *Advantages*
    * *Request batching*: Batch writes on ES cluster.
    * *Backpressure*: Consuming at its own pace.
    * *Throttling*: Slowing down if ES is overwhelmed.
    * *Retries*: Can be retries much later as Kafka will have a retention period.

**Backfill Service**
* Ingesting 100s of TBs of data in ES.
* This generally happens via a MapReduce job.
* ES cannot handle so many writes in one go. Hence, the data is written to some HDFS.
* Depending on the size of the data, workers are allocated dynamically, which take care of writing to ES.

* *Common pattern*: Defer the writes and handle in async in a non-transactional usecase. This will help in:
    * Improving latencies of the flow where the writes are happening.
    * Be able to write at our own pace.
    * Avoiding overwhelming the storage servers.
    * Be able to easily retry without impacting an latencies.