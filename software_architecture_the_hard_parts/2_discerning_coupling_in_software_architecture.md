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

* Monolith: application level change scope
* SOA: domain level change scope
* Microservice: function level change scope.

**Testability**
* It is defined as the *ease* as well as the *completeness* of testing.
* Monolith application:
    * Difficult to acheive full regression testing of all features.
* Modularity: 
    * Reduces the testing scope. Which could also be a problem.

**Deployability**
* It is not only about the ease of deployment - but also about the frequency and risk of deployment.
* Deploying changes every 2 weeks or more not only increases risk because of grouping together changes, it also leads to unnecessary delays in new critical features or bug fixes.
* *If your microservices must be deployed as a complete set in a specific order, please put them back in a monolith and save yourself some pain.*

**Scalability**
* Scalability: Ability of a system to remain responsive as user load gradually increases over time.
* Elasticity: Ability of a system to remain responsive during significantly high instantaneous and erratic spikes in user load.
    * eg. flash sales, concerts.
* Elasticity relies on services having a very small MTTS (mean time to startup) which is acheived architecturally by having very small, fine-grained services.
* Elasticity is more a function of granularity (the size of deployment unit), whereas scalability is more a function of modularity (the breaking apart of applications into separate deployment units).

* Large monolith applications are both difficult and expensive to scale because all of the application functionality must scale to the same degree. They can become quite expensive in cloud-based infrastructures.

* With service-based architecture, scalability improves but not as much as elasticity. This is becuase domains in service-based architecture are coarse grained and usually contain the entire domain in one deployment unit and generally have a long MTTS to respond fast enough to immediate demand for elasticity.

* Let testability and deployability, the more services communicate with one another to complete a single business transaction, the greater the negative impact on scalability and elasticity.
* Hence it is important to keep synchronous communication to a minimum when requiring high levels of scalability and elasticity.

**Availability/Fault Tolerance**