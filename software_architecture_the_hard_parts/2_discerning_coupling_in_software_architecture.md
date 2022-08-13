* Architects design fine-grained microservices to acheive coupling, but the *orchestration, transactionality and asycnhronicity* become huge problems.
* General advice says to decouple but does not provide any guidelines on *how* to achieve that goal while still constructing useful systems.

* Why has the complexity of distributed systems ramped up so much with microservices (we were still using event queues, etc)?
    * Now transactionality is a first-class architectural concern.
    * Prior to microservices, event handlers typically connected to single relational databases, allowing it to handle details such as integrity and transactions.
    * Moving the database to service boundaries moves data concerns to architecture concerns.

* The hard parts lie in the details, particularly how difficult parts become entangled, making to difficult to see and understand the individual parts.

* *Coupling*: Two parts of a system become entangled if a change in one might cause a change in the other.

* 1. Understand the benefits of architecture modularity
  2. Match those benefits to the issues that you are facing
  3. Analyze the trade-offs involved with breaking apart the application.

**Modularity Drivers**
* Architects shouldn't break a system into smaller parts unless clear *business drivers* exist.
* Primary business drivers:
    * Speed-to-market (or time-to-market).
    * Competitive advantage

* Speed to market is acheived through architectural agility - the ability to respond quickly to change.
    * Agility: combination of maintainability, testability and deployability.

* Competitive advantage: speed-to-market, scalability, fault tolerance.

* Note: architectural modularity does not always have to translate to a distributed architecture. Maintainability, testability and deployability can also be acheived through monolithic architectures like *modular monolith* and *microkernel*.
    * Modular monolith: Domain partitioned architecture.
    * Microkernel: Functionality is partitioned into separate plug-in components, allowing for a much smaller testing and deployment scope.

**Maintainability**
* Ease of *adding, changing or removing features*, as well as *applying internal changes* such as *maintainence patches, framework upgrades, third-party upgrades*, etc.

* Higher the incoming coupling level of a component, lower the overall maintainability level of the codebase.

* Factors affecting the maintainability level:
    * *Component coupling*: The degree and manner to which components know about one another.
    * *Component cohesion*: The degree and manner to which the operations of a component interrelate.
    * *Cyclomatic complexity*: The overall level of indirection and nesting within a component.
    * *Component size*: The no. of aggregated statements of code within a component.
    * *Technical vs Domain Partitioning*: Components aligned by technical usage or by domain purpose.

**Testability**