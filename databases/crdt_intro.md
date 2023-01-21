* Write-through cache is a great example of CRDTs. This is because a request would be considered successful if it is saved in cache. (generally faster than write back due to that reason). The database now needs to  (question: can't we use LWW here?)
* In distributed systems, we can't measure time or rely on time because it is hard to measure (different time clocks).
* Interleaving is a big problem in CRDTs.
* Uses vector clocks to solve the timestamp problem.
* CRDTs: generally 2 types:
    * state is present
    * action is present.