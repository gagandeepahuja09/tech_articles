* 

**Concurrency Control**

* SELECT FOR UPDATE ==> Pessimistic Locking
    * Controlling concurrent access to one or more rows of a table.

**Parallel Commits**
* It is an optimized atomic commit protocol that cuts the commit latency of a transaction in half, from 2 rounds of consensus down to one.
* Combined with transaction pipelining, it brings the latency down to near the theoretical commit: the sum of all read latencies + one round of consensus latency. 