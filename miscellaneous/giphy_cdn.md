**How Giphy uses CDN to serve 10 billion GIFs everyday**

* Giphy: host, serve and search GIFs.
* Serving API is relatively straightforward and efficient. JSON responses would generally be around 1-2kB.
    * Image size could be in MBs.

* Apart from caching usual static resources (eg: images, videos, JS bundle), giphy also caches API responses.
    * We can cache those API responses which are a bit static in nature. Eg: change only hourly or once a day.
        * Eg: trending API, 5 most common searches.

**Why CDN?**
* Apart from caching content, CDN provides *geographical nearness*.
    * This is very crucial for static content as the response size of the images is pretty high.
    * CDN uses edge servers which are distributed across the globe.
    * Request comes to the nearest edge server, if it has the data, it serves it. If it doesn't have the data, the request goes to the origin (generally S3), caches the data and then serves it.
    * Each edges has its independent cache.

* *How to handle viral content?*
    * The origin (S3) could get overwhelmed in such scenarios as 1000s of edge serves would be hitting S3 / backend servers in order to get the data.
    * CDNs have a **multi-layer CDN** approach to handle such problems. 
    * Rather than hitting the origin directly, they hit the shield servers which also act as cache. 
    * Shield servers are much smaller in number than edge servers and hence the number of requests going to the origin reduces.

* *Route specific TTL*
    * Depending on the pattern at which data would be getting updated, we would have different TTLs. Eg:
        * trending API: cached for smaller duration.
        * specific image: larger duration.
    * We can set the TTL based on the route pattern.

* *Response configured caching*
    * Route based caching may not specify all our needs. We might want to specify the TTL for specific kinds of requests which we can do by setting response headers: max-age and s-maxage.

* *Cache Invalidation By Grouping*
    * We might have to invalidate only certain kinds of data. Eg:
        * Invalidate cached API responses that contain a specific GIF.
            * A specific GIF might have got deleted or changed.
        * Invalidate all cached responses from an API key
            * Giphy provides SDK and API support.
            * The API key getting expired or the user getting deactivated.
    * We use surrogate keys to solve the above problem.
        * These are tags which are part of the request header.
        * Used for grouping the content.
        * Eg: cached response might be having tags for all the images.

* Todo: documentation by fastly/akamai/cloudfare or any other CDN provider.
* Push v/s pull based CDN.
