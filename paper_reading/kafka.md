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
    * It also simplifies the process of replay of messages.

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
    * Each partition corre