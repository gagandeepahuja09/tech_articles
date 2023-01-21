* https://www.youtube.com/watch?v=i8MweKYoG1U&t=312s

**Why replace elasticsearch?**
1. *Document based indexing*: Document is indexed independently on every replica. The write operation happens on every node independently. Hence scaling out is expensive as it requires scaling CPUs on all replicas.
    * A lot of work needs to be done for indexing document: processing or parsing text, stemming, ranking, putting into inverted index, etc.

2. *Uneven load distribution*: Shard distribution is managed by ES and hence load can become uneven. Manual rebalancing required in such cases.

3. *Autoscaling is challenging*: ES requires provisioning for peak load. Adding new nodes or removing some nodes requires shard migration which is expensive and trivial.

**Elasticsearch and Lucene**
* Elasticsearch is an HTTP server running on top of lucene.
* Elasticsearch makes lucene "simple" and "distributed" (cluster management).
    * Some of the key features of ES: replication, sharding, LTR (learning to rank), custom fields and analytics.

**Two Key Features Of Lucene Used By Yelp**
1. *Near-realtime segment replication*
    * Lucene has data units in a node called segments (which are immutable). Segment is created after indexing. It is copied from the primary node and replicated to the replica node rather than reindexing on every node.

2. *Concurrent Search*
    * ES has abstracted out the segments.
    * We can use Lucene to search over multiple segments in parallel and be able to leverage multiple cores.

**Implementation**
* They used open source Lucene server project which is built on top of Lucene.