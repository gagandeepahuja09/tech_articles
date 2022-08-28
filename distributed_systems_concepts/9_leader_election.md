**Raft Leader Election**
* It is implemented with a state machine in which a process is in one of the 3 states:
    * *follower state*: the process recognizes another one as the leader.
    * *candidate state*: the process starts a new election proposing itself as the leader.
    * *leader state*

* Basic condition required for a database to be used for distributed locking: it must support atomic compare and swap operation in some form + TTL (to avoid deadlocks). (Atomicity is key here: Example MySQL could do it through a combination of queries).

**How to do distributed locking?**
* https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html
* Two reasons why we might want a lock in a distributed system:
    * *Efficiency*: It saves us from doing some unnecessary computation twice. The result could be a minor increase in cost (eg: paying more to AWS) or a minor inconvenience (eg: getting the same email twice). It could actually be both in many scenarios.
    * *Correctness*: Saving from messing up the state of the system.

* If we are using locks for efficiency purpose, we might be better off using a single redis instance. (This would still be a SPOF).
* Distributed locks is a much more challenging problem compared to the regular mutexes. Why? Here we are dependent on multiple machines which can fail independently for various different reasons.

**Fencing Token**
* Let's assume that a process P0 has acquired the lock. By the time a process tries to perform the required operation, it's TTL could have expired and a new leader might have been elected. 
* Why can the above happen?
    * GC kicked in.
    * Process trying to read a page which is not in memory, so it gets a page fault and is paused until the page is loaded from disk.
    * Unexpected network delays.
* Can't we check that the current process is leader or not before performing the operation?
    * All the detays could occur later too.
* Instead we use a fencing token ==> a number that increases every time we acquire a lock.
    * If an operation with a >= number has already been performed, we discard the operation with a lower number.
* Problem with redlock: it doesn't have the ability to generate fencing tokens.