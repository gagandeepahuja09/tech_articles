* https://www.youtube.com/watch?v=BFyWl9MNDjY
* https://medium.com/booking-com-development/scaling-our-customer-review-system-for-peak-traffic-cb19be434edf

* Reviews can only be made after a booking. They are an authentic source of information and people generally don't book without reading reviews.
* Reviews is the top of the funnel. ==> Cannot go down.
* Traffic pattern: *peak of 10k RPS with p99 of 50 ms*.
* Such a low latency requirement indicates that most of the reviews need to served from cache or prematerialized views on RDBMS.

**Amount of Data**
* 250 million reviews. Each review contains:
    1. Ans to some objective questions.
    2. Ratings on various parameters.
    3. Textual feedback.
* Assuming 2kB size per review => 500 GB. This is large enough.
* Because of high amount of load and stringent SLAs, we need to:
    * shard the DB. ==> because one node cannot handle that many requests.
    * have replicas (durability) to protect again network/hardware/AZ failures. So we need to have replicas in different AZs.
* *Sharding*: Reviews will be sharded by accomodation_id so that all reviews of an accomodation are present on the same node.

**Request routing**
* Simplest way is hash based routing.
* *Challenge*: Addition or removal of nodes requires a massive data shuffle => re-partitioning the entire data.
* This is commonly solved by consistent hashing. This logic should reside at the review service to route the request to the appropriate node.
* *Practical usage*:
    1. Add or remove node.
    2. Copy the data that needs to be moved.
    3. Notify review service of the change so that it starts consuming new ring.
Question: won't there writes coming during the copy of the data?