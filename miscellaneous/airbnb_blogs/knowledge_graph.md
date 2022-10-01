* Providing contextual information.
* The knowledge graph created by Airbnb powers their search, discovery and trip planner services.
* Airbnb holds experiences, place, hotels, events, restos, markets and much more.
* We need to collate them at a single place to make them easily accessible.

* Relational databases might not be a good fit for building this because of the kind of queries as they would require very complex joins across multiple entities:
    * Find neighbourhood in LA where there are huts or islands available.

**Infrastructure**
* 3 key components:
    * Graph storage
    * Graph Query API
    * Storage Mutator

**Graph Storage**
* Graph databases are meant for very specialized usecases and they are quite operationally intensive. Those might not be required. It is also better if the team using it has some previous experience with it.
    * Operation overhead.
    * No expertise.
    * No need of very specific graph algorithms.
* Airbnb implements it with a relational database. We have to just keep in mind the two nodes and an edge. <subject, verb, object>.
* Eg. <'NEW_YORK', 'IS_IN', 'USA'>.
* Each node type has a different schema. Eg: 
    * location -> name, gps.
    * event -> name, date, venue.
* Each edge type stores nodes that connect. Eg: landmark_in_city -> landmark and city.
    * Each edge type will store the information about what types of nodes can it connect to.
* Knowledge graph is periodically dumped for offline consumption. eg: recommendation / ranking. 
    * We can't be firing query to the knowledge graph for every query.
* It should be used for offline processing.
    * Other service might have some data preloaded in cache from data warehouses of the relational database. (Eg: non-frequently updated data). Eg. Apache Pinot would gave sub-millisecond latency. We can use that, it would have high ingestion time, some lag but will have low latency and not overwhelm the graph database (via graph query API).
    * The graph query API could pass in the params what mode would it like to use: warehouse or relational.

**Graph Query API**
* Traverse the graph by specifying the path.
* Path is just a sequence of edges + data filters.
* This API would be used by any other service like search when they want to query the graph database.
* Eg: find all 'place' nodes connected with 'city' node LA with edge_type 'contains_location' such that #listing > 5000 and category = 'scenic'.
* The query could be in a simple JSON format.
* The query layer should be able to convert the JSON format query (sophisticated and nested) into a SQL query.

**Storage Mutator**
* Should be in async.