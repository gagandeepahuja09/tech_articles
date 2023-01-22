
* https://www.youtube.com/watch?v=WE9c9AZe-DY&list=PLndbWGuLoHeYTBaqFu31Nac-19qsdUl_V&index=145
**Slack Style**
* *Conservative*: Use technologies which have existed for long (> 10 years old).
* *Willing to write a little code*: Sometimes rather than telling off-the-shelf technologies, it would be better to tell the compute what to do.
* *Minimalistic*: Choose something they already operate over something new.

*Cartoon Architecture*
* Message Server, WebApp, MySQL, Job Queue 

**Login And Receive Messages**
* RTM => Real-time Messaging
* Login: POST /api/rtm.start?token=xxosds....
    * Start a session.
    * LAMP stack: Memcached: sharded MySQL.
* Data is sharded by team.
* There is a separate database which resides information about which shard a team lives on.
    * SELECT db_shard FROM teams WHERE domain = %domain;

**MySQL Shards In Slack**
* *Source of truth for most customer data*: Teams, users, channels, messages, comments, emojis, etc.
* *Replication across 2 different DCs*: Availability for 1-DC failure.
* *Sharded by team*: For performance, fault-isolation.

**Why MySQL**
* Many many thousands of server-years of working.
* Relational model is a good discipline. 
* Team experience.
* Not because of ACID. (Multi-master and various other reason compromise this for slack.)

**Master-Master Replication**
* Why do they use it and need it?
    * Write available in case of failures.
    * Master promotion should be automatic in case of failures. (Isn't this possible with master-slave?)
* How are conflicts handled?
    * If we have data sharded by team_id, there should be no conflicts as writes and reads will always happen at the same shard.
    * But actually, they might have done something more complex.
    * Most of the logic is at application-side for conflict resolution.
    * Some manually by operation action. => Edge cases where someone could be trying to update from both phone and laptop.
    * In order to make use of LWW, we can use *INSERT ... ON DUPLICATE KEY UPDATE* statement. (https://dev.mysql.com/doc/refman/8.0/en/insert-on-duplicate.html)
        * When the unique key gets violated, rather than rejecting the write, the row will get updated.
        * eg: `INSERT INTO t1 (a, b, c) VALUES (1, 2, 3) ON DUPLICATE KEY UPDATE c=c+1`.

**Login Response Payload**
* It is got a lot of information like: identity of every channel in the team, every user in the team, membership of all the channels, where the read cursor has moved in the channels we last saw (offset), etc.
`{
    "ok": true,
    "url": "some_websocket_url"
    ...
}`
* Websocket connection will provide all the latest information like: new messages, profile changes, presence information.

**Message Server**
* Message server is instead written in Java.
* It helps with write amplification to all the users.
* It doesn't have a state and directly calls the webapp for persistence.
* This is not so straighforward like a wrapper around websocket library and a for loop over the people that are connected.

**Wrinkles In Message Server**
* Race b/w rtm.start and connection to MS
    * We could miss out on the writes b/w the time that we got the response from rtm.start and actually connected to the websocket server.
    * These writes are made aware via an event log mechanism (in-memory message buffer).

* Glitches, Delays, Network Partitions while persisting:
    * We have a network boundary and a possible data center boundary. Network partitions are transient and to avoid bad user experience, we should not reject the writes in such cases.
    * This is done via both an in-memory and on-disk queue.
    * Queue depth is monitored, so that it doesn't go very high.

* Most messages are presence (offline, online). (This is N ^ 2 ==> we need to tell every user about every other user in the team).

**Deferring Work: Job Queue**
* Physically persisted in redis.
* There are multiple job queues for performance isolation. Each having different pools of workers, so it can be scaled according to the performance requirement.
* Some things take up a lot of time. Eg:
    * Link unfurling
    * Search indexing
    * Exports / Imports (importing years of data from a competing chat product).

**Other missing things**
* Memcache wrapped around many DB accesses for providing materialized views.
    * It is done on a case-by-case manner when a slow query is found and is mostly manual.
* ML Model for search results: Thrift interface.
* Rate-limiting around critical services.
* Search
    * Solr
    * Team partitioned
    * Fed from job queue workers

**Team Partition Advantages**
* Easy scaling to lot of teams.
* Isolates failures and perf problems.
* Makes customer complaints easy to field.
* Natural fit for a paid product.

**Per-Team Message Server**
* Low latency broadcasts.

**Hard Cases**
* *Mains failures*: Mains DB or group of DB which maintains the mapping of which shard belongs to which team is a SPOF.
    * Can't georeplication solve that problem? We can route the request to other datacenters in such cases.

* *Rtm.Start on Large Teams*: Consider that large teams (1000+) are trying to login at the same millisecond.

**Mains failure**
* There are 2 physical machines for mains, both are master. Both are in different data centers.
* 1 Master fails, partner takes over.
* What if both fail? Is that even possible, aren't they in different data centers?
    * It is possible if the failure is load-induced. If one went down due to load, the other would be 2X the requests.
    * Many users can proceed via memcached. For the rest, slack is down. (Can't this entire dataset be kept on memcached?)

**Rtm.Start for large teams**
* Unlike slack, can't we show old data for few users for some time.
* Can't we have rate limiting at a team level.
* Returns image of entire team.
* Channel membership is O(n^2) for n users.
* Mass reconnect
    * A large team looses, the regains office connectivity.
    * n users perform O(n^2) rtm.start operations.
    * It can 'melt' the team shard.

**Scale Out Mains**
* Mains has very simple query pattern (point queries). 
* Pick your favourite scale-out storage engine to replace mains with.
* Why didn't they do it?
    * Able to protect the mains via:
        * Rate-limiting
        * Memcached
    * Very hard and risky thing to change, which could cause a global slack outage.

**Rtm.start for large teams**
* Problem is not that bad: p95, p99: 221, 660 ms.
* One solution: *Lazy loading*
    * Since channel membership is the biggest problem, change APIs so client can load channel members lazily. Quadratic problem is not just limited to channels. (emojis, etc also).

**Mass Reconnects**
* Flannel: application-level edge cache.
    * What does edge mean? Not running very close to the data center.
    * Is this related to edge router (router located at n/w boundary that allows internal n/w to connect to external n/w s)?
    * Few of the functionalities of rtm.start will be taken care by flannel.

**Parts left out**
* Client tech: phones and laptop specific.
* Voice calls and huddle.
* Backups
* Data Warehouse
* Search