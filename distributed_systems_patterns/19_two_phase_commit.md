*Update resources on multiple nodes in one atomic operation.*

**Problem**
* When data needs to be atomically store on multiple cluster nodes, cluster nodes cannot make the data accessible to the clients before the decision of other cluster nodes is known.
* Each node needs to know if other nodes successfully stored the data or they failed.

*Comparison With Paxos and Replicated Log*
* These also have 2 phases of execution but these involve all the cluster nodes storing the same value.

**Solution**
* *Phase 1*: Ask each node it it is able to promise to carry out the update.
* *Phase 2*: Actually carry out the update.