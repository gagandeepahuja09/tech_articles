* It is a pattern of creating a pool of collections (usually TCP) and allow multiple clients to share this pool of connections.
* This pattern is particularly useful when connection establishment, connection teardown and connection security is particularly expensive, which is generally the case with databases.
* It is also useful when the server has very limited database connections and we have a lot of clients.

* Classic Way (Not recommended)
    * GET request will establish a connection at the backend, make a query and then close it.

* Correct Way
    * Spin up a pool of database connections.
    * pool.query will pick up a random connection

* Performance Benchmarking