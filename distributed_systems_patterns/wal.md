* https://www.youtube.com/watch?v=wI4hKwl1Cn4

* *Disk writes are not that straightforward*
* Before saving the write, it needs to go to the RAM -> OS Cache -> Disk Cache -> Disk.
* We can use fsync to ensure that it directly writes to the disk.
* Using fsync for each and every query would be a slow operation.
* Instead the log is updated and the actual B-tree is updated on a periodic basis.
* Append-only writes are much faster than random writes.

* *Advantages of WAL*
    * Increase in DB performance.
    * Point-in-time recovery.

* *Data Integrity In WAL*
    * There could also be data-loss while writing the WAL. The process crash in the middle of writing a new log.
    * CRC (cyclic redundancy check) is used to protect that. Checksum is the most simple form.
    * For a specific record, a CRC would be written even before the record.

* *Structure of WAL*
    * WAL consists of multiple files where each file is called a segment.
    * Size of each file is max. 16 MB.
    * Within the segment, we have pages where each page is of size 8 kB.
    * Each entry/record has a unique identifier called Log Sequence Number (LSN). Rather than having a unique identifier like auto-increment, it is the byte offset in the log file. Advantage of byte offset:
        * Easy to reach that position.
        * Database also maintains the byte offset till which the flush to the disk has been successfully completed.