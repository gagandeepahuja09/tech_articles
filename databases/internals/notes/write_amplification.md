* This is one of the reasons due to which Uber moved from Postgres to MySQL.
* Write amplification happens when the amount of data being written is a multiple of what should have been written.
* Amplification can happen at three layers:

**Application Write Amplification**
* Examples
    * Soft delete.
    * Upserts in multiple tables: todo, todo_archive, todo_count.

**Database Write Amplification**
* *Postgres Indexing*: Assume that we have a table with 5 columns and all of them have an index.
    * Any update creates a new tuple id even if one column got updated.
    * Postgres used to change the indexes to point to the new tuple.
    * HOT: Heap-only tuple solves this problem in the newer versions.
        * Old tuple points to the new tuple.

**Disk (SSD) Write Amplification**
* Charge trap, electrons, cells. ==> Very low-level.
* Limitations in SSDs which lead to write amplification:
    * We cannot override data in SSDs. We have to create a new page and mark the old page as stale. 
    * We can only delete the data in blocks in SSDs and not in pages. Hence garbage collection has to move the active pages to a new block and then delete the block.
    * B-trees have update-in-place even for insertions in tables. Hence LSM is considered better for SSDs.