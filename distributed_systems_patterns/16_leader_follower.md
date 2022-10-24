**Election Algorithm: Handling Vote Requests**
* Only the servers which are *most up to date* can be the leaders. The most up-to-date is defined by two things:
    * The latest generation clock.
    * The latest log index in WAL.
* If multiple servers are up-to-date, we can use the following criteria:
    * Some implementation specific criteria like higher id. (eg Zab).
    * If care is taken to ensure that only one server asks for a vote at a time, then whichever server starts the election before others.

* Once a server is voted for in a given generation clock, the *same vote is returned for that generation always*.

class ReplicatedLog...
    VoteResponse handleVoteRequest(VoteRequest voteRequest) {
        // for higher generation request, become follower. but we don't know the leader yet.
        if (voteRequest.getGeneration() > replicationState.getGeneration()) {
            becomeFollower(LEADER_NOT_KNOWN, voteRequest.getGeneration());
        }

        VoteTracker voteTracker = replicationState.getVoteTracker();
        if (voteRequest.getGeneration() == replicationState.getGeneration() && !replicationState.hasLeader()) {
            if (isUpToDate(voteRequest) && !voteTracker.alreadyVoted()) {
                voteTracker.registerVote(voteRequest.getServerId());
                return grantVote();
            }
            if (voteTracker.alreadyVoted()) {
                return voteTracker.votedFor == voteRequest.getServerId() ?
                    grantVote() : rejectVote();
            }
        }
        return rejectVote();
    }

private boolean isUptoDate(VoteRequest voteRequest) {
    return (
        voteRequest.getLastLogEntryGeneration() > wal.getLastLogEntryGeneration() || (
            voteRequest.getLastLogEntryGeneration() == wal.getLastLogEntryGeneration &&
            voteRequest.getLastLogEntryIndex() >= wal.getLastLogIndex()
        )
    )
}

* The server which receives votes from majority of the servers, transitions to leader state.
* Once elected, the leader continuously sends heartbeat to all the followers. If followers do not get a heartbeat in specified time interval, and new leader election is triggered.

**Leader Election Using External [Linearizable] Store**
* Running a leader election within a data cluster works well for small clusters.
* For large clusters, it's easier to use an external store like ZooKeeper or etcd. They internally use consensus and provide linearizability guarantees.
* 3 Functionalities needed for implementing a leader election:
    1. A compareAndSwap instruction to set a key atomically.
    2. A heartbeat implementation to expire the key if no heartbeat is received from the elected leader, so that a new leader election can be triggered.
    3. A notification mechanism to notify all the interested servers if a key expires. 