* Data disintegrators: Drivers that justify breaking apart data.
* Data integrators: Drivers that justify keeping data together.

**Data Disintegrators**

* *Change control*: How many services are impacted by a database table change?
* *Connection management*: Can my database handle connections from multiple distributed services?
* *Scalability*: Can the database scale to meet the demands of the services accessing it?
* *Fault tolerance*: How many services are impact by a database crash or maintainence downtime?

**Change Control**
* Breaking changes: Changing table/column/data type.
* When breaking changes occur to a database, multiple services must be updated, testedm and deployed together with the database changes.
* This coordination can quickly become both difficult and error prone as the number of separately deployed services sharing the same database increases.
* Coordinating multiple services is only half the story.