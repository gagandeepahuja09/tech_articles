**Serving Hashtags Ordered By Count**

* We will do an interesting DB optimization called partial indexes.
* Postgres: primary database.
* For each hashtag, we would be storing the media_count (photos + videos + reels).

* If we search for hashtags, we should get the result (or suggestions) ordered on the basis of most number of media.
    * Eg: snow => snowman (2M), snowwhite (1M), snowing (500k).

* Instagram uses ElasticSearch for advanced use-cases and proposes to use Postgres for this one.

**Partial Indexes**
    * If we find ourselves filtering our query by a particular characteristic and that characteristic is present in a minority of the rows, partial indexes may be a big win.

* Instagram ran the query execution plan:
    EXPLAIN ANALYZE SELECT id FROM tags WHERE name like 'snow%' ORDER BY media_count desc LIMIT 10;
* The output of the query execution plan indicated that they had to sort through 15k rows.
* Sorting is an expensive operation.
* Caching to optimize it might be a naive way of doing it.

**Long tail pattern**
* Hash tags exhibit a long-tail pattern. That is, fewer tags have large # of photos and large # of tags will have very few photos.
* Instead of going through all the hashtags, can we only go through the tags that are **popular enough**?
* Can we only *index hashtags that has more than 100 photos*?
* Postgres supports partial_index i.e. keeping only a subset of data in the index.
CREATE INDEX CONCURRENTLY on hashtags WHERE media_count > 100;
* This made the no. of rows to sort from 15k to 169.

* Note that since we passed the filter while creating the index, we need to pass that filter in the query also.

* Postgres, query planner is pretty good at evaluating constraints. If we change > 100 later to > 500, then also, it will use the right partial index.