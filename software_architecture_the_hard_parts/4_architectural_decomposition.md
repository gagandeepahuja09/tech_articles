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