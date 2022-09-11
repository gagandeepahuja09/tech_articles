* Changes to data files must be written only after those changes have been logged. That is, after logs describing the change have been flushed to main memory.
* Hence, we do not need to flush data pages to disk on every transaction commit, because we know that in the event of crash, we will be able to recover the database using the log.
* This helps reduce the no. of disk writes. Only the log file needs to be flushed to disk to guarantee that a transaction is committed.

* The cost of syncing the logs is much less than the cost of flushing all the data pages. This is especially true for small txns touching different parts of the data store. One fsync of the log file may suffice to commit many transactions.

* It also make it possible to support online backup and point-in-time recovery.