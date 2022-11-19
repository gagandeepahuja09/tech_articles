* Fully-managed NoSQL database provided by AWS.
    * Fully-managed: we don't need to run and manage our own instances.
    * You cannot run it locally or on any other cloud.
* Key advantages: consistency, predictability and reliability.
    * Consistent performance in terms of response time. (from Mbs to Pbs to data) or if you are making concurrent requests (higher TPS).
    * Predictability in terms of billing: we will be charged on the basis of the no. of units of 4kB data we read and the units of 1kB data we write.
        * That is a much easier math and planning problem than the one based on CPU and RAM.
        * We might require running load tests otherwise.
        * We will be aware of the tps at which we are getting requests currently and can easily calculate on what would happen if it gets 2x / 4x.
    * Reliability:
        * Managed by AWS: you can take it down by firing high no. of queries. 
        * Multi-tenant system. Only reason that the DB can go down is when we can have a region-wide outage in AWS.

* Original Dynamo
    * Much simpler key-value data model. (no secondary indexes) DynamoDB has a richer data model.
    * Dynamo was run like a single-tenant system. Each team would run their own instance.
    * DynamoDB: leaderless. Any of them can take writes, hence helps with availability but compromises with availability.
    * 2022: DynamoDB released a new paper.
    * Symmetry and Shared-nothing architecture: Each server has the same job. Makes the job of maintainence very easy. true with Dynamo, not true with DynamoDB? DynamoDB is operating without being symmetric because because doing the maintainence at their scale makes sense because of ammortizing a large no. of users. 

* Write Path in DynamoDB
    * Shared-infrastructure.
    * Each request to a fleet of load balancers which then goes to the request router.
    * Request router is also a fleet of services which tells the partition to be used on the basis of the partition key.
    * Each read and write request needs to have a partition key.
    * Each partition will store a maximum of 10 GB of data.
    * Each partition is replicated across replica groups. (3 replicas for each partition).
    * Each replica will be in a separate availability zone. AZs are different data center within a region.
    * Even if one AZ goes down, we have more replicas to serve the request.
    * At any given time, one of the replicas is going to be elected as a leader.
    * We will wait for quorum of writes.
    * Partitioning key should usually be something meaningful. We should avoid auto incrementing id here (why?). Reason: we need that to be done by some coordinator itself to give out those value.
    * Uuid might be fine. 
    * DynamoDB doesn't provide that level of configurability where we can play around with changing the conditions of no. of consistent reads and writes.

