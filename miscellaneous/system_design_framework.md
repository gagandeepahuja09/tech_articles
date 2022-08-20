**System Design Framework or Checklist**

**Step 1: Requirement Gathering**
* *Functional Requirements* 
    * This is one of the most complex parts. Since we are designing systems for a person and each person could be having different choices, it naturally becomes complex. 
* *Non-functional requirements*
    * Parameters like scalability, availability, resilience and the SLAs or constraints come into picture at this step.
* All of this in a real-world could be happening during the sprint grooming.

**Step 2: Capacity Planning**
* Before doing capacity planning, we need to think about the data structure on the basis of which we are planning the capacity/storage space/network bandwidth.
    * Number of requests.
    * Amount of data sent per request.
    * Amount of data stored.

**Step 3: API Design**
* It should be customer-first approach.
* What is the data the customer would be sending to me, what response would I be sending to the customer.
* Which protocol would you use: long polling or short polling?
* Long polling, short polling or web sockets.

**Step 4: Database Design**
* Don't keep the decision limited to SQL vs NoSQL. Within NoSQL, there are so many different options. We also have the option of distributed SQL, NewSQL databases.
* The problem of database design is complex because we have varying needs in an application: some operations are read heavy, while others are write heavy. Some require transactional nature, while others are analytics based. In some cases we require high consistency, while in others we might be fine with stale data. We could also be having some specific use cases like search related (elastic search), requiring specific data structures only supported in-memory (eg. redis).
* Especially at the start, we shouldn't make our systems complex by having too many databases. This will make it very hard to manage both in terms of implementation and operation. It will also make the onboarding hard, where the developer needs to be aware of multiple databases. In real-world, the database choice could also be largely determined by the databases that the team is most comfortable with.
* On many of the scenarios, we could also do benchmarking and run load tests before choosing one.
* At the start, we can choose the DB which solves most of the critical problems and for other problems, we discuss and plan the workaround.

**Step 5: High Level Design**
* Split the architecture into multiple components. We also incorporate external dependencies or dependencies with other teams.
* At these steps and all other steps, we need to keep the FR, NFR in mind.
* 3 major things in real-world system design:
    * Keeping it simple.
    * Building it as per customer needs: customer centric.
    * Making it cost-effective.
    * Resiliency: when we are just building blocks, it's easy to skip failure scenarios.
* Idempotence: We cannot make our idempotence window infinite. That would choke the storage system.
19:34

**Gathering Requirements**
* Thinking about the failure scenarios as early as possible (breaking the system in our mind asap), so that I am aware of the limitations of the system.
* Team involvement is extremely critical. When different people think with different perspectives in the team, chances of spotting edge cases are much higher.