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
    * Unlike most messaging 