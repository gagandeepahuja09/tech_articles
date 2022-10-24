**Problem**
* In a cluster of nodes, each node needs to pass metadata information it has to all other nodes in the cluster without relying on a shared storage.
* In a large cluster, if all servers communicate with all the other servers, a lot of network bandwidth can be consumed.
* Information should reach all nodes even when some network links are experiencing issues.

**Solution**
* Each node selects a random node to pass the information it has. This is done at a regular interval, say every 1 second.
* Key Considerations:
    1. Put a fixed limit on the number of messages generated per server.