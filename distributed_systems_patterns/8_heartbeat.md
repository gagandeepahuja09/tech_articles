**Large Cluster, Gossip based Protocols**
* Heartbeat mechanism doesn't scale to large clusters (100 - 1000 nodes) spanning across wide area networks. 
* Heartbeat messages would *consume a lot of network bandwidth* affecting *actual data transfer across the cluster*.
* Hence, all-to-all heartbeating is avoided.