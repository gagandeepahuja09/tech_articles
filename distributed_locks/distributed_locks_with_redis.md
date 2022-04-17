* Every library uses a different approach. Some use a simpler approach with lower guarantees compared to what can be acheived with slightly more complex designs.

*****************************************************************************

Safety And Liveness Guarantees
Minimum guarantees to use distributed locks in an effective way:
1. Safety Property: Mutual Exclusion
    * At any given moment, only 1 client can hold a lock.
2. Liveness Property A: Deadlock free.
    * Eventually it is always possible to acquire a lock, even if the client that locked a resource crashes or gets partitioned.
    * We might be using the redis property of TTL to acheive this by just automatically deleting the lock.
3. Liveness Property B: Fault Tolerance
    * As long as the majority of Redis nodes are up, clients are able to acquire and release locks.

*****************************************************************************

Why Failover-based Implementations Are Not Enough
* Set a key with a TTL(so that it eventually gets freed, property 2). When the client needs to delete the resource, it deletes the key.
* Problem: SPOF: What is master goes down? Use replica. Problem: redis uses asynchronous replication. Mutual exclusion might not hold.
    1. Client A acquires a lock in the master.
    2. Master crashes before the write to the key is transmitted to the replica.
    3. Replica gets promoted to master.
    4. Client B acquires a lock on the same resource which is held by A. ==> SAFETY VIOLATION.
* For some cases it might be fine that in failure cases, multiple keys hold a lock.

*****************************************************************************

Correct Implementation With A Single Instance

Acquire Lock: 
* SET resource_name my_random_value NX PX 30000
* NX ==> Set the key only if it doesn't exist.
* The value must be unique across all clients and all requests. Example: {timestamp}_{client_id}
* When deleting the key, we need to check if the key was created by that client only, so that they client doesn't mistakenly delete another client's key.
* When could a client try to delete another client's key? If the time has elasped and then the client tries to release the lock.

*****************************************************************************

Redlock Algorithm
* N(eg. N = 5) redis masters.
* Quorum based logic: Client needs to acquire the lock in N/2 + 1 instances.
* Also, there is a validity time / auto release time period within which the lock should be acquired.
* The client tries to acquire lock in all the instances sequentially.
* Timeout to acquire the lock(5-50 ms) << auto release time(10s) so that no time is wasted. If an instance is not available, we should try to talk with the next instance ASAP. 

*****************************************************************************

Retry On Failure

* When a client is unable to acquire a lock, it should try after a random delay(jitter) in order to try to avoid split brain condition where nobody wins.
* Faster the client tries to acquire the lock, smaller the window for a split brain condition(and the need for a retry).
* Ideally the client should try to send the SET commands to the N instances at the same time using multiplexing.
* The client that failed to acquire the majority of locks, should try to release the locks ASAP.

*****************************************************************************

Performance, Crash Recovery and fsync

* Multiplexing is the best strategy to improve performance.
* Putting the socket in non-blocking mode, send all the commands and then read all the commands later.