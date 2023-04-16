* https://www.youtube.com/watch?v=09E-tVAUqQw&t=400s&ab_channel=AsliEngineeringbyArpitBhayani
* *Why do databases store data in B+ tree?*
* Let's start simple.
    * We insert all the data in a file sequentially.
    * Relational databases store data ordered by primary key: clustered index.
    * Problem: we cannot efficiently *insert in the middle*.
        * We will also have to override the existing content that was there and then re-write everything after it.
        * The only way to do it is that we will have to create a new file copy all the contents of first half. Then insert the new content. Then again copy rest of the contents to the new file.
        * It is not like presenting enter in an in-memory buffer. When we press Ctrl+S, then it gets saved on the disk.
    * *Update in the middle*
        * If the override leads to the row taking more space, then we will have to handle the same insert in the middle problem. If takes less space, we will have to handle garbage collection or create a new file only.
    * *Find one*: Linear scan
    * *Range queries*: Possible only when rows are ordered by the attribute that we are looking for.
    * *Delete*: Create a new file without that entry or row.
    * This makes all of the operations as O(N).
    * Note LSM trees is a better, more optimal way of this naive append-only implementation. 

* *B+ Trees*
    * Rows or documents of a table are clubbed together in B+ tree nodes.
    * If 1 B+ tree node is 4KB big and doc size is 40 B.
    * Each node will hold around 100 rows.
    * Why is this 4KB size important?
        * *Size of B+ tree node = Size of disk block*.
        * What is disk block? When we do disk I/O, disk-block is the most granular width in which a read/write operation is done. 
        * In one disk read, we read 1 node or around 100 rows.
    * The row data is only present in the leaf nodes.
    * The leaf nodes might note be present one after the other sequentially. Instead, we will have offsets to go from one B-tree node to the next one.
    * All of the nodes may or may not be in the same file.