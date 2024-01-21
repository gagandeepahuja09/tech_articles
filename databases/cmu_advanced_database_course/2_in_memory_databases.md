# Background
* Much of the history of DBMSs is about dealing with the hardware limitations at that time.
* Hardware limitations earlier:
    * Uniprocessor (single-core CPU)
    * Limited RAM (much more expensive)
    * The database had to be stored on disk.
    * Disks were even slower.

* Now DRAM capacities are large enough that most databases can fit in memory.
* Why do databases occupy lesser data than we think?
    * Structured data sets are smaller.
    * Unstructured (images, videos) or semi-structured (blob) datasets are larger.

* We need to understand why we can't always use a traditional disk-oriented DBMS with a large cache (buffer pool) to get the best performance.

# Disk-oriented DBMS
* Primary location: non-volatile storage (HDD or SSD).
* The database is organized as a set of fixed-length pages or blocks.
* The system uses an in-memory *buffer pool* to cache pages fetched from disk.

# Buffer Pool
* When a query accesses a page, the DBMS checks to see if that page is already in memory:
    * If it's not, the DBMS must copy retrieve it from the disk and copy it into a frame in its buffer pool.
    * If there are no free frames, then find a page to evict.
    * If the page being evicted is dirty (modified), then the DBMS must write it back to disk.
* Why using a traditional disk-oriented DBMS with a large cache won't help. We will be going through following additional steps which are not really needed (extra work):
    * Always translate a tuple's record id to its memory location.
    * Worker thread must pin pages that it needs to make sure that they are not swapped to disk.
    * Running eviction policy to update internal metrics on how pages are being accessed. 