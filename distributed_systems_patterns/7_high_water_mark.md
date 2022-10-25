*aka CommitIndex. An index in the write-ahead-log showing the last successful replication.*

**Problem**
1. The leader can fail before sending its log entries to any followers.
2. The leader can fail after sending its log entries to some followers, but could not send it to the majority of the followers.

* Some followers can have missing entries and some can have more entries than others.
* It becomes important for each follower to know what part of the log can be made available to the client.

**Solution**

leader (class ReplicatedLog...)
private long appendAndReplicate(byte[] data) {
    Long lastLogEntryIndex = appendToLocalLog(data);
    replicateOnFollowers(lastLogEntryIndex);
    return lastLogEntryIndex;
}

private void replicateOnFollowers(Long entryAtIndex) {
    for (final FollowerHandler follower : followers) {
        replicateOn(follower, entryAtIndex);    // send replication requests to followers
    }
}

* Followers respond with the index of the latest log entry they have. The response also includes the current generation clock of the server.

follower (class ReplicatedLog...)
private ReplicationResponse appendEntries(ReplicationRequest replicationRequest) {
    List<WALEntry> entries = replicationRequest.getEntries();
    entries.stream()
        .filter(e -> wal.exists(e))
        .forEach(e -> wal.writeEntry(e))
    return ReplicationResponse(SUCCEEDED, serverId(), replicationState.getGeneration(), wal.getLastLogIndex());
}

* The Leader keeps track of log indexes replicated at each server, when responses are received.

class ReplicateLog...
    logger.info("")

*Todo: possible subtle issues*