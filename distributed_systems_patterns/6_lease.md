**Problem**
* Cluster nodes need access to certain resources.
* But nodes can crash, they can experience a process pause. Under these scenarios, they should not keep the access to a resource permanently.

**Solution**
* A cluster node can ask for a lease for a limited period of time, after which it expires.
* The node can *renew the lease* before it expires, if it wants to extends the access.

* We should implement the lease mechanism with *consistent core* to provide fault tolerance and consistency.
* The leases are replicated with the *leader and followers* to provide fault tolerance.
* It is the responsibility of the *node that owns the lease to periodically refresh it*.

* The leases are created on all nodes in the Consistent core