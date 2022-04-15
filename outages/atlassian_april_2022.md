Insights shared by Arpit Bhayani

* Doc: https://www.atlassian.com/engineering/april-2022-outage-update

Insight 1: Incremental backup strategy
* Some have reported data loss for up to 5 minutes prior to the incident.
* Data in the backup store is backed up at a frequency of 5 minutes.
* CDC Pipeline: Change Data Capture.

Insight 2: Progressive Rollout strategy
* This was for their product update: for deactivating their legacy app.
* If there are 100 customers, rollout progressively at the start for 1-2 customers.

Insight 3: Communication Gap
* Maker checker flow would have avoided it.

Insight 4: Why do we need permanent delete? 
* GDPR(General Data Protect Regulation) compliance. I have the right to be forgotten.

Insight 5: Synchronous Replication for High Availability
* Sync standby DB replica.
* Note: this is in multiple AWS availability zones. 

Insight 6: Immutable Backups for point-in-time recovery.
* Running standby instances might be very costly. This can double the DB cost.

Insight 7: Protect against data corruption
* This is via error correcting codes.

Insight 8: Not truly a multi-tenant architecture
* What we have not (yet) automated is restoring a large subset of customers into our existing (and currently in use) environment without affecting any of our other customers.
* Each customer should have an isolated and independent setup in a multi-tenant architecture.(eg. separate instances, databases, etc.)
* In case of Atlassian, having a separate DB for each customer would be very expensive and it's difficult to gain any profitability out of it.
* Most companies that clam to have a multi-tenant architecture generally have a hybrid model. For key customers they could be having a separate setup but for most of the other customers, they are generally clubbed together.


Insight 9: Why is it taking time for Atlassian to recover the data?
* Since one database stores data for multiple customers, the impact is such that customers in different databases are impacted.
* Point-in-time recovery is easy to be done for an entire table or entire database but doing that would result in data loss for customers which weren't impacted.
* So the only way could be to create separate tables with such entries and then do the insertion row by row.