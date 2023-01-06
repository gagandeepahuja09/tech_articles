* Postgres: open source. Reaching towards being the linux of databases.
    * Growth tend of Postgres popularity is much steeper.
    * From a licensing standpoint, it cannot be changed.
    * Open source allows for a global community.
    * Robust and battle-tested.
    * More than just a relational database: Time-series support, Full-text search, JSON suppport.
    * System of extensions: eg. 
        * create a stored procedure in Java.
        * REST API extension.
* Google Spanner, Amazon Aurora, YugabyteDB, CockroachDB: Postgres compliant databases.

**What does PostgreSQL compatibility mean**
* We can easily migrate from Postgres to a Postgres compatible database and if we don't like it, we can migrate back to Postgres. 
* *Compatibility levels:*
    * *Wire-level compatibility*: Reuse JDBC drivers.
        * When your application opens a n/w connection with your PostgreSQL compliant database, then all the packets that are going to be transferred b/w the database and the client application are going to be serialized in Postgres protocol.
        * *How to check for wire-level compatibility?*: You can use some DB tool like DBeaver 
    * *Syntax-level compatibility*: If we are able to execute SQL queries, joins, materialized views using Postgres syntax.
    * *Feature-level compatibility*: Let's say that we have syntax level compatibility but certain features like triggers and stored procedures are not available, then we can say that it is not feature-level compatible. It is very hard to become feature-level compatible because the feature set is very large, robust and keeps on evolving. Those databases which are built on Postgres source code will have much better feature-compatibility level. Eg: we shouldn't have to rewrite the stored procedures when shifting from one Postgres compatible DB to another.
    * *Run-time level compatibility*: We can easily migrate from one Postgres database to another.
* Maintaining features and compatibility is a much bigger challenge with distributed databases as compared to other DBs like Aurora which are not distributed.

17:32
**PostgreSQL **

**How does migration work at a high level**
1. Take snapshot.
2. Apply all those writes to happen on both databases via CDC.
3. Recon job.
    * Any tools already supported by databases to check for mismatches during migration?