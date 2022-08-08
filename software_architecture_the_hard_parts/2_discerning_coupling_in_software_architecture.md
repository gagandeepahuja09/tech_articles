* Architects design fine-grained microservices to acheive coupling, but the *orchestration, transactionality and asycnhronicity* become huge problems.
* General advice says to decouple but does not provide any guidelines on *how* to achieve that goal while still constructing useful systems.

* Why has the complexity of distributed systems ramped up so much with microservices (we were still using event queues, etc)?
    * Now transactionality is a first-class architectural concern.
    * Prior to microservices, event handlers typically connected to single relational databases, allowing it to handle details such as integrity and transactions.
    * Moving the database to service boundaries moves data concerns to architecture concerns.