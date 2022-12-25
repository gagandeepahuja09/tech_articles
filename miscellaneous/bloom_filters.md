* They are a probabilistic data structure.
* Verifies that an entry is certainly not in a set.
* There could be small % of false positives. (Bloom filter could say that entry is there but it turns out that it wasn't there).
* Usages:
    * Recommendation systems, showing Ads.
    * Used in databases: avoid looking if data is certainly not there.

* *How bloom filters works?*
* Consider we have a bitfield of size N. 
* We have a hashing function which will give a number between 0 to N-1. In the hashing function, there could be collisions. Hence a 0 would mean that an element is definitely not present while a 1 could mean that it might or might not be present.

* *Reducing the risk of collisions: and in-turn the false positives*
    * We can hash an entry multiple times with different seeds in each iteration. We will get different values for each and can hash all of the corresponding bits.
    * While checking for a key if it is present (candidate key), we can also hash it multiple times with the same seeds and even if one of them is not set, we can conclude that the element is definitely not present.

* *Accuracy of bloom filter: fill ratio*
* Fill ratio: no. of bits set in the filter.
* If the vast majority of bits are set, then the likelihood of a key returning false is decreased. This increases the false positive.

* *Scalable bloom filters*

* Sources:
    * https://redis.com/blog/bloom-filter/

