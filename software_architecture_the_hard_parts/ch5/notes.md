**Component-Based Decomposition Patterns**

* *ADR*: Architecture Decision Record.
* It's important to get it right the first, because there won't be any second time.
* Initially the composition patterns are used in sequence when moving to microservice.
* Then, they are used individually as maintainence is applied to the monolithic application during migration.

* Patterns:
    1. Identify and Size Components Pattern
    2. Gather Common Domain Components Pattern
    3. Flatten Components Pattern
    4. Determine Component Dependencies Pattern
    5. Create Component Domains Pattern
    6. Create Domain Services Pattern

* *Fitness functions for Governance*: Describes the *automated governance* that can be used after applying the pattern to *continually analyze* and verify the correctness of the codebase during ongoing maintainence.

* *Architecture Stories*: Unlike user stories which describes a feature that needs to be implemented or changed, an architecture story describes particular *code refactoring* that *impacts the overall structure of an application* and *satisfies some sort of business driver* (such as increased stability, better time to market, etc.

* Eg: *I need to decouple the payment service to support better extensibility and agility when adding additional payment types.*

* Technical debt stories usually cover things that a developer needs to do in a later iteration to clean up the code. Architecture story captures something that needs to change quickly to support a particular architectural characteristic or a business need.

**Identify and Size Components Pattern**

**Description**:
* *Purpose*: Identify components that are either too big (doing too much) or too small (not doing enough). Components that are *too large* relative to other components are generally *more coupled* to other components, are *harder to break into separate services* and lead to less modular architecture.

* The no. of source files, classes and total lines of code are not good metrics because every programmer designs classes, methods and functions differently.
* Calculating the total no. of statements within a give component can be a useful metric. (avoiding log statements).
* Statement: single complete action performed in the source code. (not a perfect metric but useful).

* Having a relatively consistent component size within an application is important.
    * The size of components in an application should fall b/w 1 and 2 standard deviations from the mean component size.
    * The percentage of code for 2 components should not vary significantly.
    * Take advantage of static code analysis tools for doing this.

* *Component Name*: Should be descriptive enough so that the roles and responsibilities are clear.
* *Component Namespace*: The physical (or logical) identification of the component representing where the source code files representing that component are grouped and stored.
* *Percent*: of the overall source code.
* *Statements*: If the statements are much larger than expected, it could possible mean that the logic is more complex than it looks.
* *Files*

* When resizing a large component, we can use a functional decomposition or domain driven approach to identify subdomains that might exist within the large component.
* Eg. Trouble ticket component (containing 22% of the codebase) can be broken down into: Ticket Creation, Ticket Assignment, Ticket Routing, Ticket Completion.

**Fitness Functions for Governance**
* Ensure that components don't get too large during normal application maintenance and create unwanted or unintended dependencies.
* These fitness functions can be part of a CI/CD pipeline.

* *Maintain component inventory*
    * Alerts for new components being added or removed.
* *No component shall exceed <some percent> of the codebase*
    * The threshold %age depends on the size and no. of components of the application. 
* *No component shall exceed <some number of standard deviations> from the mean component size*
    * Standard deviation is a good measure for determining the outliers in terms of component size.
    Standard deviation: sqrt( 1/N-1 * sum[i = 1 to n](square(xi - xmean)) )

**Case Study**
* Most of the components were about the same size except the reporting component (33% of the codebase). After some analysis it was found that there are 3 categories of reports:
    * Ticketing reports
    * Expert reports
    * Financial reports
* Common (shared) code that all reporting categories used was also identified, such as *common utilities, calculators, shared data queries, report distribution and shared data formatters*.
* Although the namespace (ss.reporting) still exists, it is no longer considered a component but rather a subdomain.