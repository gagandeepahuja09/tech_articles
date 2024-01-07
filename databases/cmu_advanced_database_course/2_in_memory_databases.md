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