* Different storage engines have different storage structures: from hashmap to sophisticated graph storage.
* Flushing to disk ==> time consuming operation. 
    * Not every insert or update to the storage can be flushed to the disk.
* Appending a file is generally a very fast operation, not impacting performance.
* At the server starup, the log can be replayed to build in-memory state again.
* We maintain a unique log identifier. Why?
    * It helps in performing multiple other operations like: Segmented Log or cleaning the log with Low-Water Mark, etc.
* The log updates can be implemented with *Singular Update Queue*.

class WALEntry...
    private final Long entryIndex;
    private final byte[] data;
    private final EntryType entryType;
    private final long timestamp;