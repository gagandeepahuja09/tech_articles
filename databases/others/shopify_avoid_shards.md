**How shopify avoids hots shards by moving data across database without having any downtime**
* https://www.youtube.com/watch?v=7v-wrJjcg4k
* Don't confuse a shopify pod with a k8 pod.
* A shopify pod is a logical grouping of a group of shops which share a common database. 2 shopify pod databases have no data in common. 
* Each table would have a column called shop_id.

* *Why do we need to move shop from one pod to another?*
    * A resource intensive shop should not take down other shops.
    * The shards (shopify pods) should have equal distribution of load.

* *How to decide which shop lives in which shard?*
* Distribution only on the basis of no. of shops won't be sufficient.
* We will apply hueretics (with help of Data science team) on the basis of:
    * Historical database utilization.
    * Historical traffic on the shop.
    * Forecasting (private request). eg: flash sale.

**Moving the shop**
* *Critical constraints*
    * Shops must be entirely available.
    * No data loss or corruption.
    * No unnecessary strain on infra. (it should not be so expensive that it puts unnecessary load on the database).

**3 High-Level Phases**
*Phase 1. Batch Copy And Tailing Binlog*
    * Opensourced: Ghostferry.
