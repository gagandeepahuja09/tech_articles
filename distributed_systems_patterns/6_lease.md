**Problem**
* Cluster nodes need access to certain resources.
* But nodes can crash, they can experience a process pause. Under these scenarios, they should not keep the access to a resource permanently.

**Solution**
* A cluster node can ask for a lease for a limited period of time, after which it expires.
* The node can *renew the lease* before it expires, if it wants to extends the access.

* We should implement the lease mechanism with *consistent core* to provide fault tolerance and consistency.
* The leases are replicated with the *leader and followers* to provide fault tolerance.
* It is the responsibility of the *node that owns the lease to periodically refresh it*.

* The leases are created on all nodes in the Consistent core, but *only the leader tracks the lease timeouts*. This is because we need the leader to decide when to expire the lease using its *own monotonic clock*, and then let followers know when the lease expires. This makes sure that *like any other decision in consistent core, nodes also reach consensus about lease expiration*.

// When a node from a consistent core becomes a leader, it starts tracking leases.
class ReplicatedKVStore...
    public void onBecomingLeader() {
        leaseTracker = new LeaderLeaseTracker(this, new SystemClock(), log);
        leaseTracker.start();
    }

// Leader starts a scheduled task to periodically check for lease expiration
class LeaderLeaseTracker...
    private ScheduledThreadPoolExecutor executor = new ScheduledThreadPoolExecutor(1);
    private ScheduledFuture<?> scheduledTask;

    @Override
    public void start() {
        scheduledTask = executor.scheduleWithFixedDelay(this::checkAndExpireLeases,
        leaseCheckingInterval,
        leaseCheckingInterval,
        TimeUnit.MILLISECONDS);
    }

    @Override
    public void checkAndExpireLeases() {
        remove(expiredLeases())
    }

    private void remove(Stream<String> expiredLeases) {
        expiredLeases.ForEach((leaseId)->{
            // remove it from this server so that it doesn't cause a trigger again.
            expireLease(leaseId);
            // submit a request so that followers know about expired leases.
            submitExpireLeaseRequest(leaseId);
        });
    }

    private Stream<String> expiredLeases() {
        long now = System.nanoTime();
        Map<String, Lease> leases = kvStore.getLeases();
        return leases.keySet().stream()
            .filter(leaseId -> {
                Lease lease = leases.get(leaseId);
                return lease.getExpiresAt() < now;
            });
    }

// Followers start a no-op lease tracker.
class ReplicateKVStore...
    public void onCandideOrFollower() {
        if (leaseTracker != null) {
            leaseTracker.stop();
        }
        leaseTracker = new FollowerLeaseTracker(this, leases);
    }

// Lease Class implementation
public class Lease implements Logging {
    String name;
    long ttl;
    // Time at which this lease expires
    long expiresAt;

    // The keys from kv store attached with this lease
    List<String> attachedKeys = new ArrayList<>();

    public Lease(String name, long ttl, long now) {
        this.name = name;
        this.ttl = ttl;
        this.expiresAt = now + ttl;
    }

    public void refresh(long now) {
        expiresAt = now + ttl;
    }

    public void attachKey(String key) {
        attachedKeys.add(key);
    }
}