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