* Time series databases are measuring data (metrics, vitals, events).
* Pinterest were using OpenTSDB to store the TS data and they ingest *millions points every second*.
* OpenTSDB is based on HBase which is based on Hadoop. Issues faced:
    1. Long GC pauses.
    2. Frequent crashes.

* The existing time series databases were not performant enough for Pinterest's needs. They created an in-house solution called *Goku*.

**Time-Series Data Model**
* Every time-series data point has 2 parts. 
    * *Metric*: We should have it verbose and keep it hierarichal so that we can apply aggregations.
    * *Tags*: They are optional. 
        * Tags are used for filtering points: exact, wildcard, regex.
* Key = (Metric + Tag), Value = (Timestamp + Value)
* tc.proc.stat.cpu.total{host=ec2-1, service=auth} = (132536457236, 860)
* Aggregators: sum, max, min, avg, count, deviation
* Downsampling: one point to represent several points.
    * Helps to reduce the granularity of the data which in-turn helps reduce the space and cost.

**Challenges And Key Decisions**
1. *Scan*: 
    * OpenTSDB scans are inefficient. They are disk-based and bucketed, which leads to a lot of random reads.
    * Goku scans are efficient: in-memory, inverted-index based.

2. *Data Size*:
    * Goku used Facebook's in-memory TSDB 'Gorilla' which gives **12x compression** out of the box.

3. *Compute And Aggregation:*
    * OpenTSFB does scatter-gather. It scatters the requests, gathers the data on one machine and then does the aggregation.
    * Goku does aggregation at two places: It does the first aggregation on the storage layer (moving the computation to the storage layer) and the 2nd one on the proxy. The results are then sent to the client. This **minimizes the data transfer over the network**.

4. *Serialization*:
    * OpenTSDB uses JSON -> slow.
    * Goku uses Thrify binary protocol to serialize.

5. *Immutable component optimized for query purposes*
    * There will be both mutable and immutable components of the in-memory storage. The immutable component is only meant for reads and the data structures used are optimized for that purpose.

**Todo: Read paper on Gorilla**