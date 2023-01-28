* Spin up two postgres instance with docker.
* Make one master, another standby.
* Connect standby to master.
* Make master aware of the standby.

* Todo: read about docker volumes.
* Setup master instance in detach mode
    * docker run --name pmaster -p 5432:5432 -v /Users/gagandeep.ahuja/Desktop/Personal\ Projects/tech_articles/databases/internals/replication/pmaster_data:/var/lib/postgresql/data -e POSTGRES_PASSWORD=postgres -d postgres
* Setup standby instance
    * docker run --name pstandby -p 5433:5432 -v /Users/gagandeep.ahuja/Desktop/Personal\ Projects/tech_articles/databases/internals/replication/pstandby_data:/var/lib/postgresql/data -e POSTGRES_PASSWORD=postgres -d postgres
* Stop both instances and copy the data 
    * docker stop pmaster pstandby
    * mv pstandby_data pstandby_data_bk
    * cp -R pmaster_data pstandby_data
    * Todo: rather than doing the actual copy, explore this and other ways to see how the replication would actually happen on production: https://www.postgresql.org/docs/current/app-pgbasebackup.html
* Start the instances
    * docker start pmaster pstandby
* Enable the replication for the user postgres in master file.
    * Note: this is not the correct practice and only done for demo purposes. Ideally we should have separate users for separate purposes.
    * cd pmaster_data
    * vim pg_hba.conf (host based authentication)
        * https://www.postgresql.org/docs/current/auth-pg-hba-conf.html
    * One copied snippet:
    # Allow replication connections from localhost, by a user with the
    # replication privilege.
    local   replication     all                                     trust
    host    replication     all             127.0.0.1/32            trust
    host    replication     all             ::1/128                 trust
    * Press i to go to insert mode.
    * Add this line at the end: `host replication postgres all md5`
        * This will allow the standby to connect to the master in replication mode.
* Config change in standby file postgresl.conf:
    * #primary_conninfo = ''                  # connection string to sending server
    * This will specify the connection details to connect to the master node.
    * `primary_conninfo = 'application_name=standby1 host=RZP1834 port=5432 user=postgres password=postgres'`
        * As we can see in the comment of the config, this is a property which is specific to standby nodes.
    * docker stop pmaster pstandby
* Create a file called standby.signal
    * This makes the instance as read-only and standby.
* Config change in master file postgresql.conf:
    * It is more like a rule like any 1 (a, b, c) or first 2 (a, b, c).
    * In our case, it will be: `synchronous_standby_names = first 1 (standby1)`
* Start and see logs
    * docker start pmaster pstandby
    * docker logs pmaster
        * Logs (master is aware of the standby): 
        `2023-01-27 14:28:07.464 UTC [34] LOG:  standby "standby1" is now a synchronous standby with priority 1`
        `2023-01-27 14:28:07.464 UTC [34] STATEMENT:  START_REPLICATION 0/1000000 TIMELINE 1`
    * docker logs pstandby
        * `2023-01-27 14:28:07.046 UTC [30] LOG:  entering standby mode`
        `2023-01-27 14:28:07.070 UTC [1] LOG:  database system is ready to accept read-only connections`
        `2023-01-27 14:28:07.220 UTC [31] LOG:  started streaming WAL from primary at 0/1000000 on timeline 1`
* Exec into the master node
    * docker exec -it pmaster psql -U postgres
        * select * from pg_stat_replication;
        * create table test(id int, t varchar(200));
    * docker exec -it pstandby psql -U postgres
        * \d test;
        * create table will give an error here.