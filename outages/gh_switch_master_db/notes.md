* Github was switching master database from one node to another.
* This led to data divergence and a production incident that lasted over 5 hours.

**Incident Report**
* Users observed delays(no data loss, only delays) --> in data being visible on the interface or API.
    * This clearly indicates us about having a master replica setup.
* Given info: *Data was written successfully but was not available for reads.*
    * This indicates that the place we write at and the place we read from were different.
    * Could this be due to replication lag being very high?

**What happens in planned database maintainence?**
* It's a planned downtime. During the restart, the writes would fail.
* Could be due to the following reasons(rebooting DB). :
    1. Apply security patches.
    2. Version upgrades.
    3. Parameter tuning: eg. switch from one index type to another. 
    4. Hardware replacement: generally done by the cloud provider. every hardware goes through wear and tear.
    5. Periodic reboots: not a common practice but it can solve or detect problem like memory leaks.
* Time conveyed by organizations for maintainence is generally with a large enough buffer time. The actual time for which the website might be unavailable is only a fraction of it.
* Github flipped their master DB(the new master should be completely in sync with the new master) because they had to do some maintainence on the old one. They keep the second instance handy.
* This is generally done by a config change.
* For a short duration during which the config flip is happening, the DB would become unavailable.
* The mysqld process of the new master crashed.
* To mitigate the problem, they redirected the traffic back to the old master.
* This solved the problem. But ...
    * The crashed MySQL server had served traffic for 6 seconds.
* In the incident report, they have not indicated on how did they solve the problem. Let's try to see how we can solve it.