*Maintain order of requests sent to a server by using a single TCP connection.*

**Problem**
* When we are using Leaders and Followers, we need to ensure that the messages b/w the leader and each follower are kept in *order*, with a *retry mechanism* for any lost messages.
* We need to do this, while keeping the *cost of new connections low*, so that *opening new connections doesn't increase the system's latency*.