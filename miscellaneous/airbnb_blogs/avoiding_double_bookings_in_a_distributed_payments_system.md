Link: https://medium.com/airbnb-engineering/avoiding-double-payments-in-a-distributed-payments-system-2981f6b070bb

* SOA poses challenges for billings and payments applications because it makes it more difficult to maintain *data integrity*.
* An API call to a service that makes further API calls to downstream services, where *each service changes state and potentially has side effects*, is equivalent to executing a *distributed transaction*.
* For transactions with multiple network calls, it is inevitable for the requests to fail at some point. 

* 3 common techniques used in *distributed systems to acheive eventual consistency*: *Read repair, Write repair and Asynchronous repair*.
* There are benefits and trade-offs to each approach.

* *Asynchronous Repair*
    * Server runs *consistency checks* such as *table scans, lambda functions and cron jobs*.
    * *Asynchronous notifications* from the server to the client are widely used in payments industry to force consistency on the client side.

* *Write repair*
    * Every write call from the client to the server attempts to repair an inconsistent state.
    * Write repair requires the client to be smarter and allows them to repeatedly fire the same request and never have to maintain state (aside from retries).
    * Clients can request eventual consistency on-demand, giving them control over the user-experience.
    * *Idempotency* is an extremely important property when implementing write-repair.

**Requirement**
* Instead of implementing a custom solution specific for a use case, we need a *generic yet configurable* idempotency solution to be used across the payments org.

* We need ultra low latency, so building a separate stand-alone idempotency service won't be sufficient. Most importantly the service would suffer from the problem it was originally intended to solve.

* While scaling organization, it would be highly *inefficient to have every developer specialize on data integrity and eventual consistency challenges*.

**Solution**
* We should be able to identify each incoming request uniquely.
* We need to accurately track and manage where a specific request was in its lifecycle.

* Orpheus library:
    * An *idempotency key* is passed into the framework, representing a single idempotent request.
    * Tables of idempotency information, always read and write from a *sharded master database for consistency*.
    * Database transactions are combined in different parts of the codebase to ensure atomicity using Java lambdas.
    * *Error responses are classified as retryable or non-retryable*.