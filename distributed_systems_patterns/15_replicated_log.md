**Problem**
Acheiving consensus on individual requests is not enough.

* For each log entry, the leader appends it to its local WAL and then sends it to all its followers.

private long appendAndReplicate(byte[] data) {
    Long lastLogEntryIndex = appendToLocalLog(data);
    replicateOnFollowers(lastLogEntryIndex);
    return lastLogEntryIndex;
}

follower (class ReplicatedLog...)
void maybeTruncate(ReplicationRequest replicationRequest) {
    replicationRequest.getEntries().stream()
    .filter(entry -> wal.getLastLogIndex() >= entry.getEntryIndex() &&
    entry.getGeneration() != wal.readAt(entry.getEntryIndex()).getGeneration())
}