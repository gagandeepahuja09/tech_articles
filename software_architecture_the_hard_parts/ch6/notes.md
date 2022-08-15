* Data disintegrators: Drivers that justify breaking apart data.
* Data integrators: Drivers that justify keeping data together.

**Data Disintegrators**

* *Change control*: How many services are impacted by a database table change?
* *Connection management*: Can my database handle connections from multiple distributed services?
* *Scalability*: Can the database scale to meet the demands of the services accessing it?
* *Fault tolerance*: How many services are impact by a database crash or maintainence downtime?
* *Architectural Quanta*

**Change Control**
* Breaking changes: Changing table/column/data type.
* When breaking changes occur to a database, multiple services must be updated, tested and deployed together with the database changes.
* This coordination can quickly become both difficult and error prone as the number of separately deployed services sharing the same database increases.
* Coordinating multiple services is only half the story. The real danger is when we forget any of the services for the table just changed. The service might become non operational.

* Consider 400 services, all sharing the same highly available clustered relational database. Imagine running to all the development teams in many areas trying to find out which services use the table being changed.
    * Also having to coordinate, test and deploy all of the services together as a single unit.

* Consider an example where service wants some data from database D part of service D. If this is behind a contract, it need not care about any changes in database D.

**Connection Management** 
* *Establishing a connection to a database is an expensive operation*.
* A database *connection pool* is often used not only to *increase performance* but also to *limit the number of concurrent connections* an application is allowed to use.
* In distributed architectures, *each service - or more specifically, each service instance typically has its own connection pool*.
* When multiple services share the same database, the no. of connections can quickly becomes saturated as the number of services or service instances increase.

* Frequent connection waits (the amount of time it takes waiting for a connection to become available) is usually the first sign that the maximum number of database connections has been reached. Connection waits also manifest themselves as connection time-out or tripped circuit breakers.

* *Example:*
    * Original monolithic application: 200 connections
    * Distributed services: 50
    * Connections per service: 10
    * Minimum service instances: 2
    * Total service connections: 1000
* The no. of connections grew from 200 to 1000.

* Without some sort of connection strategy or governance plan, services will try to use as many connections as possible, frequently starving services from much needed connections.
* We can assign each service its connection quota: either evenly distributing across all service or on the basis of the service's needs.
* Evenly distributed approach is used for the first time when the no. of connections needed by a service during peak and normal hours is not known. We can create fitness functions to measure the concurrent connection usage of each service and adjusting either manually or in any automated way.
* It mitigates connection saturation risk and also ensures that no idle connections are wasted.

* Fitness functions can be created to track how close the maximum no. of connections used is to the maximum no. of connections available.

**Scalability**
* Service scalability can put a tremendous strain on the database, not only in terms of database connections but also on throughput and database capacity.
* Once the services start to scale, the connection pool quota used earlier will be no longer valid. This will result in connection waits, which will in turn result in overall performance degradation and request timeouts.
* Breaking DB for each service will result in requiring fewer connections for each database.