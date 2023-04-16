https://kousiknath.medium.com/all-things-sharding-techniques-and-real-life-examples-in-nosql-data-storage-systems-3e8beb98830a

**Why Sharding**
* As data size becomes larger, fitting data on a single machine is not possible of becomes way too costly and tedious.

**Horizontal Sharding**: When query pattern is on the base of a certain short range. Eg: date range. We can shard the servers on the basis of date.

**Vertical Sharding**: When queries only return a subset of columns. Eg: some queries request only name and some request only addresses.

**Re-sharding**: Process of splitting an existing shard.