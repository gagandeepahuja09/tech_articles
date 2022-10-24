**Problem**
* In a cluster of nodes, each node needs to pass metadata information it has to all other nodes in the cluster without relying on a shared storage.
* In a large cluster, if all servers communicate with all the other servers, a lot of network bandwidth can be consumed.
* Information should reach all nodes even when some network links are experiencing issues.

**Solution**
* Each node selects a random node to pass the information it has. This is done at a regular interval, say every 1 second.
* Key Considerations:
    1. Put a fixed limit on the *number of messages generated per server*.
    2. The messages should not consume a lot of *n/w bandwidth*. Upper bound of around a few 100 kBs, making sure that applications' data transfer is not impacted by too many messages across the cluster.
    3. The metadata propagation should *tolerate a few n/w and server failures*.

* For epidemics or rumors, if n is the total no. of people in a population, it takes interactions = log(n) per individual. log(n) can be treated as a constant.

class Gossip...
    Map<NodeId, NodeState> clusterMetadata = new HashMap<>();

class NodeState...
    Map<String, VersionedValue> values = new HashMap<>();

* At startup, each cluster node adds the metadata about itself, which needs to be propagated to other nodes.
* Metadata example: IP address, port that node listens to, partitions it's responsible for, etc. 

* Startup ==> added in constructor itself.
class Gossip...
public Gossip(InetAddressAndPort listenAddress,
            List<InetAddressAndPort> seedNodes,
            String nodeId) throws IOException {
                this.listenAddress = listenAddress;
                // filter this node itself in case its part of seed nodes
                this.seedNodes = removeSelfAddress(seedNodes);
                this.nodeId = new Node(nodeId);
                **addLocalState(GossipKeys.ADDRESS, listenAddress.toString());**

                this.socketServer = new NIOSocketListener(newGossipRequestConsumer(), listenAddress);
            }