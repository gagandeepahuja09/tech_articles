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

**How to test in production (like) environment**
* Running load tests on production is very hard. Teams need to prepare for months. Every team needs to have switches to turn off if something unexpected happens. How to remove the useless data after the load test?
* Why do we need to run load tests on production? Most companies don't have the luxury to run a parallel infrastructure to production to simulate the production traffic.
    * Expertise required for: building above, managing it and ensuring that to be cost optimal.
* How to run load test on production? Create a separate DNS route-53 endpoint for that. Start with very small traffic.
    * We will need to have clear identifier of whether some data got inserted due to load test, so that it can be cleaned up later.
* Testing load of stateless components is much easier. It is the stateful components like databases or any other storage engines or message queues which are a challenge.

**Replicating the production pattern**
* Eg. we see a traffic pattern of sinusoidal wave in traffic, we will need to replicate that via some tools. You can also replay the request logs, which would be getting populated through ELK stack.

**How to make sure you are testing the right thing?**
* In most cases, the database is the problem. First fire raw SQL queries and then in the application context.
* Understand the core limitations of your tech stack.
* Check whether your language is single threaded or multi-thread. 
* Test for synchronization, whether code is able to handle concurrent request via mutexes / locks.
* Understand your critical routes or flows which need to be test or load-tested every time or frequently. Identify critical reads and critical writes ==> these need to be tested in every deployment.

**Longevity Testing**
* Running load tests for a longer duration.
* It can help identify memory leaks in our program.
* The leak could be so small that in a single day, it cannot even be identified. Only after a few days, we see a slight increase in memory.
* Simple example: setting a key in redis without a TTL.
* We will need to run this with a sustained load on a parallel setup to identify this.
* A startup might just reboot the system, if it solves the problem in the short term. Eg. running a script to restart if the memory goes beyond a threshold.
* Memory leaks are not easy to identify. It could also be the case that there is no memory leak in our code but some library or package or any vendor that we are using is leading to memory leak.

**Security Testing**
* Cannot be leaking PII like account details, aadhaar, pan details, birth date, email, etc.
* Facing a data breach could break down the entire reputation of the brand in a day.
* Opensource: Prowler, cloud custodian. Can give whole list of info like leaked subdomains.
* Handling encryption.

**Chaos Testing**
* Injecting some known failures and seeing how our system reacts to it.
* Eg. retries handle properly, circuit breaker working properly.
* Helps in checking whether failure in a subsystem is not leading to the entire system going down.
* Most services are cloud-native. They take the cloud services for granted. Eg. if s3 is down, many services start getting impacted directly.
* Here too, data remaining consistent is a key requirement.
* Companies can use basic features of chaos testing to test for data consistency.
* Make communication asynchronous by default.

**Key metrics to monitor a DB server**
* CPU, memory, Disk usage, Cache hit ratio, Query execution plan, frequent queries, infrequent but slow queries, IOPS.
* Disk usage is a key metric to be measured.

**Key metrics for API server**
* CPU, memory are very common.
* CPU, memory, no. of requests per second, network utilisation.
* We cannot undermine measuring the network utilisation. The system could be network heavy and we could assume that since CPU, memory utilisation are low, we can scale down the number of nodes.

**Metrics for async worker**
* No. of messages in the message broker.