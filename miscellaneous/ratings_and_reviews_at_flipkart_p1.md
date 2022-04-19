Ratings & Reviews @ Flipkart Part1

* If products = 10M => product reviews (10 * 100)M.
* Available in vernacular languages.
* Revamp => data size reduction = 90%, throughput inc = 5x.

High-level architecture
* Moderation pipeline => ML + human moderation. => Ranking
* Reads(100,000 RPS) => 1000x writes(100 RPS).
* Writes stored in RDBMS.
* Reads => KV store => First 10 reviews to be shown are materialised(materialised views) and stored in KV store.
* 1TB => review data.
* 5x inc in reviews and 15x languages => 75 TB of data.

Data Optimisation
    * Data Cleanup
    * Data Serialisation
    * Data Compression
    * Data Deduplication

Data Cleanup
Key Learning: When data grows, data size is more important than uniform read & write interfaces.
* Many of the fields might not be getting used in the read path. eg: accountId.


Data Serialisation
* JSON => Human readable => Verbose & slow to parse.
* Field names take a good chunk of space => 30-40% space.
* Instead of putting limiters for demarcation, we keep the length of each field encoded in the data and use it for demarcation.
* Complex data types, enums, decimals would be handled differently.