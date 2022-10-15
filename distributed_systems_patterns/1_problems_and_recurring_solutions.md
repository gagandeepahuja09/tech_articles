**Problems And Recurring Solutions**

**Process Crashes**
* WAL and replication.

**Network Delays**
* In TCP/IP protocol stack, there is *no upper bound on delays* caused in transmitting messages across a network.
* It can vary based on the *load of the network*.
* A 1 Gbps network link can get flood with a *big data* job that's triggered, *filling the network buffer*, which can cause arbitrary delays for some messages to reach the server.

* In a typical data-center, *servers are packed together in racks*, and there are *multiple racks connected by a top-of-the-rack switch*.
* There might be a *tree of switches connecting one part of the data center to another*.
* It is possible that a set of servers may or may not be able to communicate with each other. This is called *network partition*.

* *How to know that a server has failed?*

* Two problems to be tackled here:
    * A particular server *cannot wait indefinitely* to know if another server has crashed.
    * There should not be *2 sets of servers*, each considering the *other set to have failed* and hence continuing to serve different sets of clients. Causing a split brain problem.

* To tackle the first problem, every server sends a heartbeat message to every other server. If a heartbeat is missed, the server sending the heartbeat is considered crashed.
* Heartbeat interval is small enough to ensure that it does not take a lot of time to detect server failure.
* In the worst case, the server might be up and running, but the cluster as a group can go ahead considering the server to be failed.

* With the split brain problem, it 2 sets of servers accept update independently, different clients can get and set different data and once the split brain problem is resolved, it is *impossible to resolve conflicts automatically*.
* Every action that the server performs can only be considered successful only if the majority of the servers can confirm the action.
* If we want to tolerate f failures, we need a cluster size of 2f + 1.

* Quorum makes sure that we have enough copies of data to survive some server failures. But it is *not enough to give strong consistency guarantees to clients.* 
* If the write operation only succeeds on one of the server, only it will have the latest value. *High-water mark* is used to solve that problem.
* A *high-water mark* is used to *track the entry in the WAL that is known to have successfully replicated to a quorum of followers*.
* All the entries upto the high-water mark are made visible to the clients.
* The high-water mark is also propagated by the leader to the follower, so there are no inconsistencies seen by the client if the leader is down.

**Process Pauses**
* Processes can pause arbitrarily. Eg: GC pauses.
* During a long GC pause, a new leader would have gotten elected and have started processing writes.
* After the GC pause of the old leader is over, it would need to propagate writes which couldn't be processed at the time of GC pause. If we try to pause such requests as-is, it might lead to overwriting of some of the updates. 
* Generation clock is used to mark and detect request from old leaders via a monotonically increasing generation number.

**Unsynchrnonized Clocks And Ordering Of Events**
* The problem of detecting older leader messages from new ones is a problem of *maintaining ordering of messages*.
* We cannot use system timestamps for maintining the ordering of messages because the *system clocks across servers are not guaranteed to be synchronized*.
* A time-of-the-day clock in a computer is managed by a *quartz crystal* and measures time based on the *oscillations in the crystal*.
* The mechanism is error prone as the crystals can oscillate faster or slower and so different servers can have very different times. The clocks are synced via NTP which checks via global time servers.
* This time is also based on assumptions due to network delays.

* To solve all these problems, we use Lamport clocks. Generation clock is an example of that.

* *Lamport Clocks* are used for ordering events.
    * They are just numbers which are incremented only when an event happens in the system. In a DB, these events are reads and writes.
    * The lamport clock numbers are also passed in the messages sent to other processes.
    * The receiving process can select the larger of the two numbers, the one it receives and the one in maintains.
    * This way, lamport clocks track *happens-before relationship b/w events across processes which communicate with each other*. Example of this: servers taking part in a transaction.

* While lamport clock allows ordering of events, it does not have any relation to time-of-the-day clock. We use *hybrid clocks* to bridge that gap. (it maintains both system time and logical time). 

* The lamport clock allows determining the *order of events across a set of communicating servers*. But it *does not allow detecting concurrent updates to the same value across a set of replicas*. *Version vector* is used to detect conflict across a set of replicas.