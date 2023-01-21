Source: https://www.youtube.com/watch?v=KTJ4sqAgcxA&t=864s&ab_channel=TheGeekNarrator

* How to store data, how to process it, how to make the query faster, how to expose the data to the user?

**Open Source**
* Apache community.

**Basic Anatomy Of A Search Engine**
* Google is a free form search engine. We can type anything we want and google will interpret its *intent*.
* In addition to the optimizations that they have done around indexing, high availability, a sizeable amount of compute power goes only into understanding the *user intent* and decorating it with *metadata*.
* The semantic nature of the search will result in different architectural decisions. Eg: 
    * Uber will require doing geolocation search (lat, long) in absolute realtime.
    * Amazon: product relevance.

* **Search Flow**
* *Crawler*: A way to be able to incrementally collect the information from the source.
* *Repository/Storage*
* *Cleansing and Enrichment Layer*: Crawlers will get dirt information. Crawlers need to be lighweight as they are dealing with large amounts of data, hence they don't do cleaning on their own. We should be able to filter out the information that we want and not store everything. Else it will affect the time and memory.
* Building a web crawler is a challenge because of the scale.
    * We also have to capture the delta for the pages already crawled. We cannot crawl again.
    * How to maintain the freshness of the data?
    * Page repository is not the only source of truth. We need to update the index and metadata as well.
    * Apache Nutch, Tika: examples of Open source web crawler.
    * *Cleansing and Enrichment Layer*: Eg. google will go different result for the same user. Location, past searches, etc are different.
    * Most common data structure associated with any search engine is "inverted index" and "terms dictionary".
    * For each term, we could be maintaining the documents in which it is present.
    * We could also be maintaining the frequency of the no. of times a term was present in the document or the positions where it was present in the document or even both.
    * Apart from that, there are other indexes: quad trees, tries, kd trees, columnar store.
    * Index is a push process instead of a pull process. Messages could be microbatches in message queue and then sent.
    * Page repository is holding the documents.  

* **Search Engine Components**
* *Overseer*: It is looking at the entire cluster and its health. Which nodes are alive or dead. Handling failover. What jobs are running or failed. "Housekeeping Operations".
* Storage and compute can be coupled or decoupled. Coupling will help in better performance. Cost, performance, query pattern are key factors which will decide whether to keep storage and compute on same or different nodes.
* Worker nodes could be responsible for both indexing or search. Or we could have separate nodes or indexing and search.
* We will face competition of resources for search and indexing.
    * Search: CPU, Memory bound (how?)
    * Indexing: CPU, Network, Memory (at times) bound (how?)
* Request -> API Engine -> Traffic Cop -> Scheduler.
* Scheduler talks to the coordination store to get the health of the system.
* Worker could do the following: parsing, apply some NLP techniques like stemming and some analysis. We will then break down the data into indexes.
* *Most search engines maintain the data in an append-only format.*
* There is only 1 segment open in memory at a given time. As soon as segments are created and flushed to disk, they can be replicated to the subsequent replicas.
* Which means we can keep shipping the segments to the replicas even when the indexing is ongoing.
* *Schema-on-write or schema-on-read*. Schema-on-write means that we need to define the schema before we start indexing.
* *Query and Ingestion Isolation*
    * When we have separate nodes for query and indexing, in those scenarios, the storage and compute are generally decoupled. We require a shared storage for interaction.
    * If the index worker nodes know, where to ship the segments after they are built. That is, index nodes and query nodes are aware of the partitioning scheme. This could create a problem where we need to have a very high network link open b/w the peer nodes. We could have a dense network where every index nodes is able to connect to every query node or maintain some mapping which might not go well with ephemeral networks.
    * Solr solves this problem by creating *request quotas*. Eg: a node can handle 100 concurrent requests, out of which 40 are dedicated search and 60 are dedicated index requests. This is tweakable. Eg: we would want maximum capacity to go to search in day time and to index in night time.
    * If we are doing the dynamic allocation at a cluster level, it needs to be done very careful as if it goes wrong, it could lead to resource starvation and could impair the ability to dynamically resize the cluster.
    * Where is the configuration for resource quota stored? Overseer checks for updates in the configuration or it could be an event driven system where the event is sent to the overseer and it updates the coordination store.
    * Workers periodically pull the configuration from the coordination store, ensuring that they don't overwhelm the coordination store. It is not a good idea to push the configuration all the time in a large cluster due to fan out. (53:02)
* *Pros and cons of append-only systems*
* Pros
    * Lock-free: writers don't block readers.
    * Allow to scale well.
* Cons
    * Updates: we use tombstones. We have to read backwards. Document state in the latest segment only matters but we will be paying for all the segments where that is present.
    * This leads to I/O, latency, cost problem.
    * We use merge to solve this problem. (similar to GC). Problem: expensive for I/O, CPU.
* *Hotspots*:
    * We can have predictable (eg. upcoming concert or flash sale) or unpredictable hotspots.
    * We can take measures in advance to mitigate predictive scenarios.
    * For unpredictable hotspots, decoupling of storage and compute could solve the problem. If there is too much pressure on a single shard, we can have multiple workers read the same shard. The bottleneck could be the storage where we are not storing on those storage nodes for a long time.
    * Hotspot could also be a read or write hotspot. In case of read hotspot, we could just increase the no. of workers.
    * Write hotspots are harder as it generally requires going to a master and then replicated to replicas. We could have this by having dynamic partitions: split the hot partition itself or go to a leaderless replica mode (we will have to handle conflicting writes in such scenarios).
    * There are also solutions like *lazy quorums* where other nodes which were not responsible for saving writes also save the write for it on a temporary basis. Once the load on the shard stabilizes, they can handoff the new data which they had stored temporarily.
    * We also have the concept of *virtual sharding* used at certain places. We could virtual key ranges, which could move around if required.
    * *Will batching writes help in case of hotspots?* It does work if the # of objects being updated is not large. Possible problems:
        * *stale writes*
        * *Maintainence*: High in-memory maintainence.
        * *Reliability*: node goes down, will we write transactional logs for in-memory buffers.  
* *How does the storage happen?*
    * It is stored on the local disk by the worker along with the local disk of the replica responsible for that shared.
    * *Tiered storage*: Latest shards live on worker nodes for a certain duration. Then they move to worker nodes with cheaper and slower storage like HDDs and eventually they are compacted and moved to a cold storage like S3 or HDFS.
    * ES: https://www.elastic.co/guide/en/elasticsearch/reference/current/index-lifecycle-management.html Critical for cost saving.
* *Query processing*
    * Unlike regular databases, we cannot rely rely on the sharding schema to prune away shards. Eg: we will know the exact shard to go to depending on the query (hash or range partitioning).
    * Search engines have a much higher fanout. We can implicit do the pruning by devising some scheme by understanding the intent of the user but there is no defined way of doing it.
    * Typically, coordinate worker node queries all other worker nodes and ranks and finds the relevant ones.
* *Ranking*
    * It is generally a multi-phase operation.
    * Phase 1: static ranker. Only look at docs with static rank > 100.
    * Phase 2: TF IDF/ Cosine similarity.
    * Phase 3: Nueral networks. (not part of core search engines).
* *Filter queries*
    * Range query handling: Lucene uses K-D Trees.
* Workers are not dealing with the actual documents. They will only return the uuid and the rendering layer will take care of getting the docs.
* *In-memory indexes*
    * Before flushing the data to disk, we keep the data in-memory and search engines combine the results of in-memory and disk indices.

* *Operational aspects*
    * What if one of the node goes down?

* Ingestion Layer --> Enrichment Layer --> (Indices, Metadata for Indices) --> Query Engine --> Ranking.

* Key Components
    * Question: whether we want to keep the query processing and indexing on the same or different node?
    * Search engines have different architectures depending on the usecase: Cost, query pattern. Some keep storage and compute colocated for better performance while other decouple it. These are more distributed system problems rather than search problems.
    * Search engines will be facing competition of resources between search and indexing.
        * Search => CPU, memory bound.
        * Indexing => CPU, network, memory bound.
    * There are usecases like labels and annotations to tag whether a node is only for query processing or indexing. This gives the end-user the flexibility.
    * Most search engines keep their data in an append-only format. Hence it is easy for us to do active-active replication.
        * As soon as the in-memory segments are created, they can be flushed to their subsequent replicas. This allows sending the segments to the replicas even as the indexing is going on.

* How does an index look like?
    * The segments may or may not be of the same size. Only maintaining the schema on write or schema on read is important. Schema on read is more complex and less efficien than schema on write but it is more flexible.
    * Request Quotas used in Solr: Given a node's provision capacity, it can serve 100 concurrent requests.
        * 40 are dedicated search requests and 100 are dedicated indexing requests.
        * This allows flexibilities depending on workloads. Eg: day time: more focus on querying and less focus on indexing. night time: more focus on indexing.

* Challenges with LSM trees
    * There could be multiple copies of the data. That is, the updates would lead to creation of tombstones. We will always need to check the latest segment if there is a tombstone for it or for getting the latest value.
    * Merging and compaction can solve this problem but it is a very expensive operation like garbage collection and could be competing resource with the query processing and indexing.

* Query processing
    * Search engines will have much larger degree of fanout because we are not certain on the shard in which our data will reside.
    * We can still prune the partitions. Eg. only use the Germany partition.
    * Lucene has KD trees which allows us to do efficient range indexing.