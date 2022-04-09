* Capacity planning is required based on expected traffic patterns.
* Disabling non-critical flows by the services.
* QoS is a way of doing graceful degradation while servicing API requests. Eg. showing payment reminder takes higher priority than promotional offers.

* Traffic management can be done at both client-side and server-side.
* Server-side is generally done by setting rate-limit of various APIs.

* In client side based traffic management, the client decides whether to route the traffic to server or not.
Circuit breaking(reactive): Prevent from performing operations that is doomed to fail. It will only get into action when the target service has started to degrade.

* QoS is a much more proactive way of handling it which involves doing a lot of benchmarking beforehand and setting up certain pre-defined thresholds.
* More than 10X spike seen in a span of 30 seconds.
* By the time the circuit breaker would have detected it, the damage would have been already done. Eg. DB overload, services slowing down, etc.

COMPARISON

Trigger
    * Ckt breaking: Current health of target service(error rate, latency, etc).
    * QoS: Pre-defined parameters like req/s.

Scope
    * Ckt Br: Local, doesn't require a global view of parameters.
    * QoS: Requires a global view of the requests supported by a target service.

Pros
    * Ckt Br: Simpler to implement as a global view is not required.
    * QoS: Prevents the target from degrading by setting predefined thresholds.

Cons
    * Ckt Br: Only kicks in when the service has started to degrade.
    * QoS: 
        1. Perf testing => Needs E2E benchmarking of a target service to determine failure threshold.
        2. Static in nature. Benchmarking needs to be a continuous exercise. 