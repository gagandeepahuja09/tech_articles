Source: https://www.youtube.com/watch?v=KTJ4sqAgcxA&t=864s&ab_channel=TheGeekNarrator

* Ingestion Layer --> Enrichment Layer --> (Indices, Metadata for Indices) --> Query Enginer --> Ranking.

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