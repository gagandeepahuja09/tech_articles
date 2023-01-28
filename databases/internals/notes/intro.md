Concepts
* Table 
* Row_id
* Page
* IO
* Heap data structure
* Index data structure B-tree

**Table** 
* Logical representation of data.
* Storage model only understands bits.

**Row_id/Tuple_id**
* Postgres maintains an internal field called row_id. In MySQL, it is the same as primary key.

**Page**
* Depending on the storage model(rows and columns), the rows are stored and read in logical pages.
* Pages are fixed size memory or disk locations.
* The database doesn't read a single row. It reads a page or more in a single I/O and we in turn get a lot of rows.
* Each page has a size. (8kB in postgres, 16kB in MySQL) (configurable).
* Unlike RAM, disk is not byte addressable.

**I/O**
* I/O operation is a read request to the disk.
    * We also have to deserialize the bytes in order for the DB to process, which is an expensive operation.
* We try to minimize this as much as possible.
* An I/O can fetch one or more pages depending on the disk partitions and other factors.
* An I/O cannot read a single row, its a page with many rows in them.
* I/Os are expensive. We want to minimize their number.
* Some I/Os in OS go to the OS cache and not disk.

**Heap**
* Heap is a data structure where the table is stored with all its pages one after the other.
* Traversing the heap is expensive because we need to traverse each and every page.
* Indexes will help us in telling what pages of the heap we need to pull.

**TODO: Read more about Clustered Index and IOT**
https://learn.microsoft.com/en-us/sql/relational-databases/sql-server-index-design-guide?view=sql-server-ver15

**Indexes**
* An index is a data structure that has pointers to the heap.
* It has a part of the data and is used for quickly searching something.
* Indexes tell us exactly which page to fetch in the heap instead of taking the hit to scan every page in the heap.
* Indexes are also stored as pages and it costs I/O to pull the entries of the index.
* The smaller the index, the more it can fit in memory and faster the search.
* Popular data structure for index is B-tree.

**Clustered Index**
* The heap table can be organized around a single index. This index is called clustered index of IOT (index organized table).
* There can only be 1 clustered index. In MySQL, primary key is the clustered index and other indexes point to the primary key "value".
    * The selection of the PK is the key as the heap would be organized on that.
    * UUID which is truly random decreases the write performance.
* Postgres only has secondary indexes and all indexes point directly to the row_id.