* Dirty Reads: Reading uncommitted changes. It could be rolled back.
* Non Repeatable Reads: We read the same value in a transaction twice and its value changed the second time. This could be undesirable.
* Phantom Reads: The same query was executed twice. The first time it gave empty result and the second time it gave some result (because it didn't exist the first time). Example: range query of a certain date.
* Lost Updates: Lets say that you updated something. This wasn't committed. Some other transaction updated that information. This is an example of lost update.

* https://dev.mysql.com/doc/refman/8.0/en/set-transaction.html
* https://www.percona.com/blog/2020/07/27/generating-numeric-sequences-in-mysql/

**Dirty Reads**
* Default MySQL isolation level is repeatable read:
    * SELECT @@GLOBAL.transaction_isolation, @@GLOBAL.transaction_read_only;
    * SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
        OR SET [GLOBAL/SESSION] TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;
* `WITH RECURSIVE seq AS (SELECT 1 AS value UNION select value + 1 FROM seq WHERE value <= 100) SELECT * FROM seq;`
* INSERT INTO TEMP WITH ...;
* BEGIN both transactions
T1
`
    SELECT sum(t) FROM temp; ==> 5151
    update temp set t = t + 5 WHERE t = 101;
    select sum(t) from temp; ==> 5156
`

T2
`
    select sum(t) from temp; ==> 5156
`

T1
`
    ROLLBACK
`

T2
`
    select sum(t) from temp; ==> 5151
`
* SET GLOBAL TRANSACTION ISOLATION LEVEL READ COMMITTED; ==> try all of them again.

**Non Repeatable Read**
* Repeat the above exercise but COMMIT instead of rollback.
* We ran the select query twice for T2 and saw that the results were different. This could cause some inconsistency and would be better to have a consistent view of the database throughout the transaction.
* Databases solve this through MVCC.
    * This is expensive.
    * Any update ==> create a new row and soft delete. => maintain created by and deleted by where both of them are transaction_id. Postgres implements it this way.
    * MySQL and oracle use a different way. They maintain the delta/undo stack. (you can check more on this).

**Phantom Reads**
* Results generally with queries which give more than 1 result. (which is very common).
* SET GLOBAL TRANSACTION ISOLATION LEVEL REPEATABLE READ;
* Instead of updating an existing value, a new value got inserted.
* Why do we differentiate b/w the two? non-repeatable and phantom? the implementation would be different. we can consider using locks for non-repeatable read. (I didn't get it)

T1
`
BEGIN;
select sum(t) from temp; ==> 5156
`

T2  
`
BEGIN;
select sum(t) from temp; ==> 5156
`

T1  
`
insert into temp values(101);
select sum(t) from temp;    ==> 5257
COMMIT;
`

T2  
`
select sum(t) from temp; ==> 5156
`