* *Elephant migration anti-pattern*: Eating the elephant one bite at a time may seem like a good approach at the start, but in most cases it leads to an *unstructured approach*, leading to distributed monolith.

* We need to take a holistic view of the application and apply either *tactical forking* or *component based decomposition*.

* Architectural Modularity      ==> Why
* Architectural Decomposition   ==> How

* Which approach is the most effective?
    * One of the main factors in selecting a decomposition approach is how well the existing monolith application is structured.
    * Do clear components and component boundaries exist within the codebase or is the codebase largely an unstructured big ball of mud?

**Is the Codebase Decomposable?**
* Event handlers wired directly to database calls and no modularity can be considered a Big Ball of mud architecture.
* There could be tools to help determine macro characteristics of a codebase, particularly coupling metrics, to help evaluate internal structure.

**Afferent and Efferent Coupling**
* Afferent coupling measures the no. of incoming connections to a code artifact (component, class, function, etc).
* Efferent coupling measures the outgoing connections to other code artifacts.
* Virtually every platform has tools that allow architects to analyze the coupling characteristics of code in order to assist in restructuring, migrating or understanding a codebase. eg. JDepend - Eclipse Platform. Try to search something similar for PHPStorm.

**Abstractness and Instability**
* Abstractness is the ratio of abstract artifacts (abstract classes, interfaces, etc) to concrete artifacts (implementation classes). (abstract vs implementation).

* Instability is ratio of efferent (outgoing) coupling to the sum of both efferent and afferent coupling.
* It determines the volatility of a codebase, high degrees of instability breaks more easily.
* Instability reflects how many potential changes might be forced by changes to related components.
* Close to 1 => highly unstable.
* Close to 0 => either stable or rigid. It is stable if it comprises mostly abstract elements and rigid if it comprises mostly concrete elements.
* The trade-off for high stability is lack of reuse - if every component is self contained, duplication is likely.
* Thus it is better to look at the value of I and A combined rather than looking at them in isolation.

**Distance from the Main Sequence**
* D = | A + I - 1 |
* *Zone of uselessness*: Too far in the upper right. Code that is too abstract becomes difficult to use.
* *Zone of pain*: In the lower left. Code with too much implementation and not enough abstraction becomes brittle and hard to maintain.

* If while evaluating the codebase, many components fall either into the zone of uselessness or pain, it might not be a good use of time to maintain and improve the internal structure.

**Component-Based Decomposition**
* Most of the difficulty and complexity involved with migrating monolithic applications to microservices comes from *poorly defined architectural components*.
* When breaking monolithic applications into distributed architectures, *build services from components, not individual classes*.
* When migrating to microservices, *we can consider moving to a service-based architecture first as a stepping stone*.

**Tactical Forking**
* Restructuring architectures that are basically big balls of mud.
* When we think about restructuring a codebase, we thinking of extracting pieces.
    * Due to the tight coupling, it can happen that while extracting a component, we discover that more and more of a monolith must come along because of dependencies.
* Steps:
    1. Give each team a copy of the entire codebase.
    2. Start deleting the code that you don't need rather than extracting the desirable code. Devs find this easier in a tightly coupled codebase because they don't have to worry about extra the large no. of dependencies that high coupling creates.
* Note: Unless developers undertake additional efforts, the code inside the newly derived services won't be better than the chaotic code from the monolith.
* The name is apt. It is tactical and not strategic.