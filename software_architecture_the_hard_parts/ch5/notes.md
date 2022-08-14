**Component-Based Decomposition Patterns**

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