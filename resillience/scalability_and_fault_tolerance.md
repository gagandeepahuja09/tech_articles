https://www.youtube.com/watch?v=IGPBWljXjLI&ab_channel=TheGeekNarrator

**Scalability**
* Able to handle large no. of concurrent users without degrading the performance.
* Cost is also a key parameter, we shouldn't always require increasing the no. of nodes to a scale. We could have built the system in a non-optimal way due to which we are requiring large no. of resources.
* *Real system design is always cost-driven design.*
* *Sustainability is critical to the success of product.*

**Fault Tolerance**
* Fault tolerance is not just about the visible failure.
* No failure in the system should break the correctness of the data.
* *Context is King. Think about sustainability first, which depends on the stage of your organization.*

**Be as pessimistic you can. Think about failures**
* After every single line of code, assume that your infra could break and see if you are still in a consistent start of not.
    * ALL kinds of failures: network, disk, memory, process, etc.
    * Are my DB queries running in a transaction?
* Scalability and fault tolerance go hand-in-hand. Being able to handle one and not the other is of no use.
* *Always think in baby steps. Be very explicit. Tell the system what exactly needs to be done.*
    * Eg. Design an image upload service. Instead of just saying that I'll take image and directly upload to S3, we could say:
        * My server would send a request to S3 to get the signed URL.
        * After getting the signed url, we can upload from both frontend and backend. 

**How to hide system failures from customers?**
* We will need to build some abstractions.
* *User-experience plays a key role here.*
* QoS (Circuit Breaker) Example: flash sale. Rather than showing a spin loader screen, when we can't handle the traffic, we should instead not even allow users to come in after a certain limit has reached. For eg., if we have a limit of 100k phones, if no. of users > X * 100K, we will put them in waitlist or ask them Go as items are finished and not let them affect the backend APIs. 
* In most cases, we think of circuit breaker as being a good neighbour to an external service or an internal service, but this is a sort of circuit breaker for the end customer.
* *Always have a fallback plan.*
    * Eg. show estimates, if due to load, you cannot show the exact details.

**How to prove that our system is scalable? What is the limit of our one machine?**
* We should know the limit of our machine running a particular service under a specific load.
* This is critical for capacity planning. Allows to find out the number of required machines and whether we will be able to handle certain scale?
* We need to bombard the system with 1 million requests. One machine won't anyway be able to handle that. With one node or machine, we will be able to find the magic number (TPS).
* With proper monitoring and observability setup, we can exactly know where our potential bottlenecks are.
* In order to make our system, it is necessary to quantify it.
* We should go in detail and figure out those bottlenecks, but there is always a balance which needs to be maintained with the deliverables.