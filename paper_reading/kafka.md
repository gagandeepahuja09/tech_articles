**Why traditional enterprise messaging systems don't tend to be a good fit for log processing?**
1. They focus on providing a rich set of *delivery guarantees*.
    * Delivery guarantees are generally an overkill for collecting log data.
    * Eg: loosing a few page view events or counting a few page view events twice is not the end of the world.
    * These unrequired features increase complexity of both the API and the underlying implementation.

2. They don't focus on throughput as the primary design constraint.
    * Eg: JMS has no API to allow the producer to explicitly batch multiple messages into a single request. This means that each message requires a full TCP/IP roundtrip.

3. Weak on distributed support
    * There is no way to partition and store messages on multiple machines.
    * They assume near-realtime consumption of messages, hence the queue of unconsumed messages has to be fairly small. This is not the case in case of some failures in the worker or for data warehouse applications which require batch load.

**Traditional Log Aggregator**
* Other log aggregator services aggregate the log entries and periodically dump them to HDFS.
* Most of these systems are built for offline use and often expose implementation details unnecessarily (eg. minute files) to the client.
* **Push vs Pull Model**
    * Most of these systems use push model.
    * Kafka finds pull model better because the consumer can consume the messages at its rate and avoids being overwhelmed.
    * It simplifies the process of replay of messages.
    * Simplifies the data maintained at broker. Broker need not maintain offsets for each broker and smartly handle purging of logs.

**Basic Terms**
* *Topic*: A stream of messages of a particular *type*.
    * A producer can publish messages to a topic.
* The published messages are stored on a set of servers called *brokers*.
* The consumer can subscribe to one or more topics from the brokers.
    * It consumes the subscribed messages by pulling data from the brokers.
* Message: payload of bytes.
    * Serialization to encode the message.
    * Batching of multiple messages for efficiency.

Sample producer code:
`
    producer = new Producer(....);
    message = new Message("test message".getBytes());
    set = new MessageSet(message);
    producer.send("topic1", set);
`

* A consumer creates one or more message streams for the topic.
    * The message published to that topic will be distributed into sub-streams.
    * The message iterator stream never terminates. If there are no messages, the iterator blocks until new messages are published to the topic.
* Kafka supports both **Point-to-point and Pubsub**
    * Point-to-point delivery: If there are multiple consumers of a topic, only one of them would receive the message.
    * Publish/subscribe: If there are multiple consumers of a topic, all of them would get their own copy of the message.

* **Distributed**: Since Kafka is distributed in nature, a Kafka cluster consists of multiple brokers.
    * To balance load, *a topic is divided into multiple partitions*.

**Efficiency on A Single Partition**

* **Simple Append-Only Storage**
    * Each partition of a topic corresponds to a logical log.
    * Physically a log is implemented as a set of segment files of approx the same size. (eg. 1 GB).
    * Every time a publisher publishes the message, the broker simple appends the message to the last segment.
    * *Flushing the segments to disk*
        * For better performance, segment files are flushed to disk only after a configurable number of messages have been published or a certain amount of time has elapsed.
        * Database on the other hand, needs to update the wal for each and every write query.
        * A message is exposed to the consumer only after it has been flushed.
    * *Offsets*
        * Unlike other messaging systems, it doesn't maintain an explicit message id.
        * Each message is addressed by its logical offset in the log.
        * This avoids maintaining indexes mapping message ids to the actual message locations. These indexes would be seek-intensive and random access in nature.
        * Message ids are increasing but not consecutive. The next offset can be found by adding the length of the message to the current offset.
    * *Offset consumption at consumer*
        * The consumer issues asynchronous pull requests to the broker to have a buffer of data ready for the application to consume.
        * Each pull request contains the offset of the message from which the consumption begins and an acceptable no. of bytes to fetch.
    * *In-memory offset index*
        * Each broker keeps in-memory a sorted list of offsets. These offsets are the the offset of the first message in every file.
        * Offset of the 1st msg of file N = offset of last message of file (N - 1) + the message size. 

**Efficient Transfer**
* Producer: Batching of messages.
* Consumer: Although the end consumer API iterates one message at a time, under the covers, each pull request consumes multiple message upto a certain size, typically hundreds of kilobytes.

* *Effective Caching*: Kafka avoids in-memory caching and relies only on page (OS) caching.
*Pros*
    * Avoid double buffering.
    * Warm cache is retained even when the process restarts. (?)
    * *No garbage collection dependency*: Garbage collection is very time and resource intensive. Not caching in memory, reduces the garbage collection overhead. This makes the Kafka implementation possible in a VM-based language.
    * *Sequential access patterns make normal OS caching methods very effective.*

* SendFile API: reduces data copies and system calls. (TBD)

**Stateless Broker**
    * Unlike most messaging, the broker doesn't maintain the information on how much each consumer has consumed.
    * This reduces a lot of complexity and overhead on the broker.
    * This makes it tricky for the broker to delete the message since it doesn't whether all subscribers have consumed the message. This is solved by time based SLA (generally 7 days) for the retention policy. No message will be retained more than this period. It doesn't care whether the consumers were able to finish consumption in this period.
    * Kafka's performance doesn't degrade with a larger data size, hence the retention is possible.
    * *Side benefit*: 
        Rewinding back to old offset and re-consuming data is much simpler. Useful in case of application-level errors for replaying certain messages.

**Distributed Coordination**
* Producer can send a message to a randomly selected partition or on the basis of a partitioning key and a partitioning function.

* **Consumer Group**: Each message is delivered to only one of the consumers with the group.
    * No coordination is needed across consumer group.
* *Goal*: 
    * The consumers with the group can be in different processes or in different machines.
    * Our goal is to divide the messages stored in the brokers evenly among the consumers, without introducing too much coordination overhead.
* *Solution 1*:
    * If we try all the consumers with the CG to read all the message from a partition, then we would require taking locks and maintaining information regarding the consumer who was the first to acquire the lock so that other consumers don't read the same information.
* *Solution 2*:
    * Instead we solve this problem by making partition the smallest unit of parallelism. This means that only one C from a CG can consume from a partition at a time.
    * Consuming processes need to coordinate only when the consumers re-balance the load which is an infrequent event.
    * In order for the load for the load to be truly balanced, we require many more partitions in a topic than consumers in each group. 

* **No central master node**
    * Avoids SPOF and handling master failures.
    * Consumers coordinate among themselves in a decentralized manner. 
    * Kafka makes use of ZooKeeper for coordination: A highly-available consensus service.

* **Zookeeper**
    * It has a simple filesystem like API.
    * Operations supported: Set the value of a path, Read the value of a path, Delete a path, List the children of a path.
    * Few interesting features:
        1. One can register a watcher on a path and get notified when the children of a path or the value of the path changes.
        2. We can create ephemeral paths, which means that it gets automically removed if the creating client is gone.
        3. Zookeeper replicates its data to multiple nodes which makes the data highly reliable and available.

* **Kafka + Zookeeper**
Kafka uses Zookeeper for following tasks:
1. Detecting the addition and removal of brokers and consumers.
2. Triggering a rebalance process in each consumer when the above happens.
3. Maintaining the consumption relationship. (the consumers for each topic).
4. Keeping track of the consumed offset of each partition.

* When a consumer or broker starts up, it stores its information in a broker or consumer registry in Zookeeper.
* *Broker registry* stores:
    * Broker's host name and port.
    * Set of topics and partitions stored on it.
* *Consumer registy* includes:
    * Consumer group to which it belongs.
    * Set of topics that it subscribes to.