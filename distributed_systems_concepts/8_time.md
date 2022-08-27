* It is easier to grasp the flow of execution in a single-threaded application since every operation appears sequentially in time, one after the other.
* In a distributed system, there is ***no shared global clock*** that all processes agree on and can be used to order their operations. To make matters worse, processes can run concurrently.
* It's challenging to build distributed systems that work as intended without knowing whether one operation happened before another.
* *Family of clocks* to work out the order of operations across processes in a distributed system.

**Physical Clocks**
* A process has access to a physical wall-time clock.
* *Vibrating quartz crystal:* 
    * It is *cheap, but not accurate*.
    * It can run slightly faster or slower than others depending on *manufacturing differences* and the *external temperature*.
* *Clock drift:* The rate at which a clock runs.
* *Clock skew:* The difference b/w 2 clocks at a specific point in time.
* Because quartz clocks drift, they need to be synced periodically with higher accuracy clocks like *atomic clocks*.
* Atomic clocks measure time based on quantum-mechanical properties of atoms and are signigficantly more expensive than quartz clocks. They are accurate to 1 second in 3 million years.

* The Network time protocol is used to synchronize clocks.
    * The challenge is to do so despite the *unpredictable latencies introduced by the network*.
    * A NTP client estimates the *clock skew* by correcting the *timestamp received by a NTP server* with the *estimated network latency*.
    * All the estimates make it error prone. Eg: an operation that executed after another could appear to have executed before.

* *Since we don't have a way to synchronize wall time clocks across processes perfectly, we can't depend on them for ordering operations.*

* We need to look at the problem from a different angle. *Happened-before* relationship creates a *causal bond* between 2 operations. One that happens first can change the state of the process and affect the operations that comes after it.

**Logical Clocks**
* The simplest posible logical clock is a counter, which is incremented before an operation is executed.
* For multiple processes, when one process sends a message to another, a so called synchronization point is created.
* Lamport clock algorithm:
    * Counter := 0 (initialization).
    * The process increments its counter before sending an operation.
    * When a process sends a message, it increments its counter and sends a copy of it in the message.
    * When a process receives a message, its counter is updated to 1 plus the maximum of its current logical timestamp and the message's timestamp.
* Crash recovery can be supported by persisting the clock's state on disk.

* Note: If operation O1 happened before O2, then the logical timestamp of O1 < O2. But the converse cannot be guaranteed with Lamport timestamp. Eg: E could have before or after C in the diagram.

**Vector Clock**
* It is a logical the guarantees that if 2 operations can be ordered by their logical timestamps, then one must have happened before the other.
* It is implemented as an array of counters, one for each process in the system. Each process stores its own local copy of the array.
* Given 2 timestamp vectors, T1 and T2 if 
    * every counter in T1 <= every counter in T2
    * atleast 1 counter in T1 < corresponding counter in T2, then O1 happened before O2.
* If 2 operations can't be ordered. Eg: E and C, they are considered to be concurrent.

* Sometimes using physical clocks could be fine when we don't require strict ordering. Eg: timestamp for logs.