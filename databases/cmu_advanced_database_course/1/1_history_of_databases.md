(39.58)
https://www.youtube.com/playlist?list=PLSE8ODhjZXjasmrEd2_Yi1deeE360zv5O

* A lot of issues that the databases were facing in the 1960s and 70s are still relevant today.
    * How to run transactions correctly.
    * How to maintain indexes.
* *History repeats itself.*
* SQL vs NoSQL database debate is reminiscent of Relational vs CODASYL (Network data model).
    * Spoiler: Relational model almost always wins.
* The only exception could be machine learning.

# 1960s
* *Network data model (GE: IDS)*
* Tuple-at-a-time queries.
* We need to apply nested for loops to find the parent and the child.
    * Complex queries: low-level for loops.
    * Membership sets can easily get corrupted.
* Supplier -> supplies (2 columns: parent, chield) -> supply -> supplied_by (parent, chield) -> price.

* *Hierarchical (IBM: IMS: Information Management System )*
    * Still in use. Many ATMs still use this.
    * Programmer defined physical storage format.
        * We could define the data structure that we would want to preserve the data on disk. Some sort of hash table or order preserving tree.
    * Tuple-at-a-time queries.
* Problems
    * Duplicate data.
    * No independence
        * Earlier I used hash table but later I realize I need range queries. I have to dump all the data and load it as B+ tree.

# 1970s - Relational Model
* Seeing the problems of developers rewriting programs every time the schema or layout changes, Ted Codd from IBM came up with relational model:
    * Store data in simple data structures.
    * Access data through high-level language. (QL => SQL)
        * Back then, these ideas seemed controversial. C => high-level language. People though that should be written in assembly language.
    * Physical storage left upto implementation.
* *Instead of tuple at a time, apply hash-joins.*