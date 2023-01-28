* *How shopify moved from UUID to ULID and saved 50% on write performance*
    * MySQL uses clustered-index.
    * The data is organized around the clustered index (it is the key for B-tree).
    * B-tree is an ordered data structure. Hence the page for ordered data will reside close to each other.
    * If we are using a random id, then we are doing random writes while in case of sorted id, it will be sequential writes as the write would always come to the same or next page. 
    * On the other hand, in case of random uuid, we might have to go to an old page which will be a random write.
