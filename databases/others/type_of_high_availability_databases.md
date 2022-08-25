* https://www.cockroachlabs.com/blog/brief-history-high-availability/#where-to-from-here

**Fault Tolerance vs High Availability**
* High availability can be considered an aspect of fault tolerance.
* A system can be highly available but not necessarily fault tolerant.
* Fault tolerance implies *zero service interruption*. If there is a failure somewhere in the system, it will switch to the backup solution immediately.
* Eg: A system could be returning a response but that could be buggy or inconsistent where consistency is a necessity. This is available but not fault tolerant.

* *Problem with Active-Passive Availability*
    * If active node dies, some data would be lost which was not replicated in async replication. In sync replication, availability would be bad because in order to serve writes, both active and passive nodes need to be available to satisfy writes. (latency would also get affected).

* *Problem with Sharding*
    * *Operational and engineering burden on team*: Increases the problems by 1.
    * In many cases, the routing of the shards could be so complex that it that the routing ends up creeping into an application's business logic. Eg. Require significant (sometimes even monumental) engineering effort to modify how a system is sharded.
    * Coordinating transactions across shards is so complex that most systems avoid it completely.

**Active-active availability**
* These systems didn't support transactions or strong consistency but are significantly easier to manage.
* *Because each server could handle reads and writes for all of its data, sharding was easire to accomplish algorothimically and made deployments easier to manage*.
* Whenever a node received a write, it would propagate the change to all other nodes that would need a copy of it. Situations where 2 nodes received the write for the same key are handled by conflict resolution algorithms.

**Consensus Replication**
* A system that would guarantee consistency but would also provide high availability.
* Writes are proposed to a node and then replicated to some no. of other nodes. Once majority have acknowledge the write, it can be committed. (sync repl for the majority of the nodes).