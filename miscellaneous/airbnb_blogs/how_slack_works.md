
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