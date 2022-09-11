* Transactions provide an *illusion* that a group of operations that modify some data have *exclusive access* to it and either *all* operations execute successfully or *none* does.
* Transactions that update data owned by multiple services are challenging to implement.

**Concurrency Control**
* Optimistic concurrency control doesn't block. It checks for conflicts only at the very end of the transactions.