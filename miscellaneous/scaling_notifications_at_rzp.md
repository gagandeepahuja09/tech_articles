* Meeting the SLAs is very crucial here.
* Notification system could include: email, SMS, Push messages and Webhooks.
* Just after a transaction, we could be sending email to the customer and push message + webhook to the merchant.

**Existing Notification Flow**
* They could be checking the message delivery by calling the notification vendor's API or by relying on webhook.
* Limitation: p99 goes to 2-4 seconds.
* *Challenges while scaling*
    1. Read load on DB during peak.
    2. Scaling of worker POD is limited to IOPS of the database.
        * There is a limit to the number of IO operations that the database can handle.
        * If the number of concurrent connections that the database can handle is 500 and the number of workers is 300, then the workers won't be able to scale.
        * Databases are not elastic, they need to be provisioned very well.
        * We have to keep the number of database connections which would be required at peak load.
    3. Surge during special events were hard to handle.

**Rearchitecting Notification System**

1. *Prioritizing Incoming Load*
    * Not all notifications are equal - Transactional >> Marketing
    * One type of notification should not affect others.
    * We will have 3 priorities of queues: P0, P1, P2 queue.
    * There would also be a 4th queue: rate-limited events queue.
        * Each queue, event, customer has some configurable rate limit, breaching which the message goes in a separate queue.

2. *Reducing Database Bottlenecks*
    * In order to reduce the bottleneck on the database, we will write to the database asynchronously.