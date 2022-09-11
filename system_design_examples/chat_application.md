**How will you handle the problem of concurrent messages in a channel?**
* Optimistic Locking: problem of too many retries. (MVCC)
* Pessimistic Locking: too slow.
* Timestamp ordering: We are using timestamps for conflict resolution. We can maintain the ordering upto millisecond of latency. If messages are beyond, this we need not maintain 

**How will we index the messages?**
* ES likes it when the documents are indexed in bulk.
* A worker grabs a bunch of messages and indexes them in a single bulk operation.