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

***************************************************************************************************

Dirty Reads And Writes

Dirty Reads: If txn B reads a value written by txn A before it txn A is committed.
Dirty Writes: If txn A, B are concurrently writing to the same set of rows and txn B writes after A and overwrites what is written by A before A is committed.

* Both would lead to data inconsistency as both would be reading or overwriting a value which might get rolledback.

***************************************************************************************************

Read Uncommitted Isolation Level
* One of the weakest levels.
* As the name suggests, it allows txns to read uncommitted values in the presence of concurrent write transactions.
* If the txn would have rolled back, it would lead to an inconsistent state.
* Undesirable hence most DBs don't support this isolation level.
* Doesn't address any of these problems:
    * Dirty Reads
    * Dirty Writes
    * Lost Updates
    * Non-repeatable reads
    * Phantom reads

***************************************************************************************************

Read Committed Isolation Level
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