Source: https://www.youtube.com/watch?v=9iAJjtvBwyI&ab_channel=AsliEngineeringbyArpitBhayani

Horizontal Sharding: Split a table by rows and keep them on separate servers.

Vertical Sharding: 
* Distributing a database across multiple machines. eg. all payment related tables go in one DB server and all authentication related tables in another server.
* Note: we are not splitting, we are distributing.
* This is mostly required when moving from monolith to microservice.
* Example: We have 4 tables in the database: T1, T2, T3, T4.
    * Shard 1 => T2
    * Shard 2 => T1, T4
    * Shard 3 => T3
* Apart from monolith to microservice, the other common use case is for better load handling. Moving a table from 1 shard where the load is higher to a shard where the load is less.

Problem Statement: Moving a table from 1 database server to another with minimal downtime.

Picking a configuration store
* Zookeeper will have all the meta information with it about which table is present in which database. Some of the reasons for using it:
    * Pubsub like reactively flowing the information to all API servers.
    * Security benefits and simplified config changes.

Steps:
1. Dump the table along with binlog position using mysqldump(official utility provided by MySQL). The dump will have the entire data of the table along with the binlog position(like commit log ==> every operation that gets performed in the DB gets logged in the binlog file).

2. Restore the dump to another database. Load dump.sql to DB2.

3. Note: Since we are trying to avoid any downtime, the main database would also be accepting writes even during the time we are restoring the dump to DB2. 
    * For this, we need to ensure via a replication job that all changes are flown to DB 2 as well.
    * We will require writing our own job and in most cases won't be able to use MySQL's default replication. Hence the binlog position is crucial.
    * Eventually both the databases for the given table will come in sync.

4. Once other database DB2 is almost caught-up, at this point we have to do a cutover. That is, move all the traffic from DB1 to DB2.
    * If the replication lag between the two databases for that table is very low, eg. .0001 (available in the statistics)
    * *Step 1* Rename the table in DB1. Now the inserts would start giving table not found error.
    * *Step 2* Update the entry in Zookeeper to now say that table T2 is now present on DB2.
    * *Step 3* Zookeeper reactively sends information to all API servers using watch.
    * For the duration between step 1 and 3, we will get table not found errors. 
    * Since the replication was very minor, the table T2 will very quickly catch up.
    * For huge table, it becomes risky because DB1 and DB2 might never come in sync because of large amount of writes. That is, replication lag will always be there.
