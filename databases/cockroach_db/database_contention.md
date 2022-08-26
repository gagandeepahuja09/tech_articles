* Lock contention happens when *multiple processes* are trying to access the *same data at the same time*.
* Eg in SQL database: Multiple txns trying to update the same row at the same time.
* Serializable isolation is the strongest isolation level and the only one that completely ensures data integrity. Such kind of isolation levels require "locks" so that multiple transactions are not trying to access the same data at the same time.

* *Example of database contention*
    * Database contention issues are seen only at a large scale. Example: viral video, each row trying to increment that value by 1 of the same row which gives the count.
        * Possible solution: batching of the writes if strong consistency is not required. But this might not be possible for all cases.

* *Diagnosing Database Contention*
    * *Checking performance and error message*: RETRY_WRITE_TOO_OLD, RETRY_SERIALIZABLE.
    * *Querying internal tables to find contention*:
        * SELECT * from yourdb.crdb_internal.cluster_contended_{indexes/tables}; 
    * Graphs in DB console: 
        * SQL statement contention graph.
        * Transaction restarts graph.

* *Best Practices*:
    * Break up larger transactions into smaller ones if possible.
    * Use SELECT FOR UPDATE for transactions that will be reading a row and then updating the same row.
    * When replacing values in a row, use UPSERT rather than a combination of SELECT/INSERT/UPDATE.

* *SELECT FOR UPDATE*
    * It locks the rows returned by the select query. The lock will only be released once the update is performed and the transaction is committed.
    * Locking + queuing ensures that no thrashing occurs.
    * *Wait policies*: These determine how a `SELECT FOR UPDATE` statement handles conflicts with locks held by other transactions.
        * *Default*: Rows that are locked by a transaction must wait for a transaction to finish.
        * *SKIP LOCKED*: Skipping locked rows is not yet supported in CRDB.
        * *NOWAIT*: It returns an error if a row cannot be locked immediately. 