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
    * If the index worker nodes know, where to ship the segments after they are built. That is, index nodes and query nodes are aware of the partitioning scheme. This could create a problem where we need to have a very high network link open b/w the peer nodes. (48: 08)


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