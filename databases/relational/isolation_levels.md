Isolation Levels Explained

Consistency
    * Client-specific property of a transaction.
    * Represents the DB transitioning from one valid state to another preserving database constraints. eg. unique, refrential integrity.
    * Weaker guarantee since provided by the client and not the database.
Isolation
    * Defines visibility semantics of concurrently running transactions.
    * Describes how and when should parts of a concurrently running transaction be visible to other transactions.

Isolation Levels
* Important to understand implications.
* Helps in debugging concurrency bugs.
* Helps to understand use-cases of each as well as the performance implications.

***************************************************************************************

Dirty Reads And Writes

Dirty Reads: If txn B reads a value written by txn A before it txn A is committed.
Dirty Writes: If txn A, B are concurrently writing to the same set of rows and txn B writes after A and overwrites what is written by A before A is committed.

* Both would lead to data inconsistency as both would be reading or overwriting a value which might get rolledback.

***************************************************************************************

Non-Repeatable Reads(Read Skew)
* When executing a txn we read the same row multiple times and get different results for these rows.
* This could be problematic in real-world scenarios where we are seeing different results and different points in time. We might want a snapshot. Example: long running processes like migration.

***************************************************************************************

Phantom Reads
* It is an extension of non-repeatable reads.
* Non-Repeatable => When reading the same set of rows, returns the same no. of rows but different results.
* Phantom Reads => When reading the same set of row, returns different no. of rows which happens when rows are INSERTED or DELETED btw subsequent txns.

***************************************************************************************

Write Skew
* It's a specific case of lost update problem.
* Eg. booking application.
* 2 txns check to see if the row is available. It's available for both of them.
* Ideally the 1st txn should have won but here the latter txn wins.

***************************************************************************************

1. Read Uncommitted Isolation Level
* One of the weakest levels.
* As the name suggests, it allows txns to read uncommitted values in the presence of concurrent write transactions.
* If the txn would have rolled back, it would lead to an inconsistent state.
* Undesirable hence most DBs don't support this isolation level.
* Doesn't address any of these problems:
    * Dirty Reads
    * Dirty Writes
    * Lost Updates
    * Non-repeatable reads(Read skew)
    * Phantom reads

***************************************************************************************

2. Read Committed Isolation Level
* Default for Postgres.
* Ensures that there are no dirty reads and dirty writes.

Implementation
Prevention of Dirty Reads
* It prevents dirty reads by keeping a max of 2 copies of data: both uncommitted & committed value.
* The uncommitted value can only be used by the ongoing transaction.

Prevention of Dirty Writes
* Using row-level locks on the rows which a txn will be modifying.
* Other concurrent txns will have to wait until the 1st txn commits/aborts and releases the lock.

Problems not addressed:
    * Non Repeatable Reads
    * Phantom Reads

***************************************************************************************

3. Snapshot(Repeatable Read) Isolation Level ==> MVCC(Multi-Version Concurrency Control)
* Default for MySQL.
* Basic Idea
    * Every txn reads all the committed rows required for executing reads and writes before the start of the transaction.
    * Every operation in txn reads for this consistent snapshot.
    * The decision of conflict resolution on the rows concurrently modified is made at the time of commit.

Implementation
* Maintains multiple versions of the same rows at a given point in time, due to multiple concurrent txns.
* Each row in the table has 2 hidden fields: created_by and deleted_by which indicates the txn that created and deleted that row respectively.
* Since multiple versions need to be maintained at a given point in time, periodically the DBMS runs a garbage collection process & removes deleted & unreferenced entries from the DB freeing up space.

***************************************************************************************

4. Serializable Isolation Level
* Solves phantom reads & write skew.
* Both phantom reads & write skew can be solved if txn were executed one after the other.
* Most stringent isolation level.
* Most DBs don't support it as the default isolation level due to performance implications.
* It doesn't mean that all txns run sequentially internally. It just means that the output of executing txns is same as if the txns were running sequentially.

Implementation: There are 2 ways of implementing it
* 2PL(Pessimistic Locking)
* SSI(Optimistic Locking)

***************************************************************************************

2PL(2 Phase Locking)(Pessimistic)
* Using locks to ensure that txns block other txns from accessing the same data during their lifecycle.
* Multiple txns acquire shared locks and read the same rows concurrently.
* In order for the txn to write, it has to acquire an exclusive lock and wait for all shared locks to be released.
* Similarly if a txn has acquired exclusive lock, all reads must wait for the exclusive lock to be released before acquiring shared locks.
* 2 Phases:
    Expanding Phase: Locks are acquired and no locks are released.
    Shrinking Phase: Locks are released and no locks are acquired.
* Downside: Performance

***************************************************************************************

Serializable Snapshot Isolation(Optimistic)
* Relatively new. Developed in 2008 and part of Postgres 9.1.
* On top of snapshot isolation, SSI adds a layer of serializability for detecting conflicts while aborting and committing txns.
* It avoids the performance related issues with 2PL.

***************************************************************************************

Lost Update Problem(Read-Modify-Write Cycle)
* In case of 2 concurrent txns, one can override the other's value.
* Eg. both read, inc, write. Expected inc by 2 but actually got incremented by only 1.
* Since this is a common DB problem, many solutions are available for this:

* Atomic Updates
    // MySQL
    UPDATE users SET counter = counter + 1 where user_id = :user_id
    // REDIS
    INCR key
* Compare And Swap(CAS): The update should happen only if the previous value matches.
    UPDATE user SET counter = 5 where user_id = :user_id AND counter = 4
* Explicit Locking: For certain scenarios atomic updates and CAS cannot be applied when we have a group of operations. In such scenarios, we can do this via explicit locking by specifying the lock in the query.