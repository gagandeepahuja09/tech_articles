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
    * One copied snippet:
    # Allow replication connections from localhost, by a user with the
    # replication privilege.
    local   replication     all                                     trust
    host    replication     all             127.0.0.1/32            trust
    host    replication     all             ::1/128                 trust
    * Press i to go to insert mode.
    * Add this line at the end: `host replication postgres all md5`
        * This will allow the standby to connect to the master in replication mode.