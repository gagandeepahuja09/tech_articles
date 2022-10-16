**Consistent Core**

**Maintain a *smaller cluster* providing *stronger consistency* guarantees to allow *large data cluster* to *coordinate server activities* *without implementing quorum* based algorithms.**

**Problem**
* Larger the data size, more no. of nodes we require in the cluster.
* There are some common requirements in a cluster which require *strong consistency guarantee: linearizability*. The implementation also needs to be *fault tolerant*. Eg:
    * Selecting a server to be the master for a particular task.
    * Managing group membership information.
    * Mapping of data partitions to servers.
* In quorum-based systems, throughput degrades with the size of the cluster.

**Solution**
* A separate data cluster can use the the small consistent store to manage metadata and for taking cluster wide decisions with primitive like *Lease*. 