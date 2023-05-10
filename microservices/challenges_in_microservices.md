Source: https://www.youtube.com/watch?v=yTSq6hJFmUg&ab_channel=AsliEngineeringbyArpitBhayani

1. Managing Microservices
    * We always talk about the benefits of microservices, but the grass is not always green.
    * Defining the scope of a service also becomes critical. 
        * A microservice should not be too small otherwise we will have far too many microservices to manage.
        * It should not be too large, otherwise it will go into macro monolithic architecture.
    * A new microservice should be well planned. It should be a well though through decision on whether we really need a microservice for this and if we do, then what should be the scope of it.
    * Instead of building tooling from scratch, use existing tools. If some util can be used across organization, open source it.


2. Monitoring and Logging
    * There could be blindspots in the microservice where we are not aware of the dependencies to other microservices.
    * Debugging a root cause and spanning services should be easy. Distributed tracing becomes super critical for this. eg. Zipkin, OpenTelemetry, Jaeger, Hypertrace, etc.

3. Service Discovery
    * With their being 100s of microservices spread across 1000s of servers, how would you know which server to talk to for getting the required work done.
    * It's not as straightforward as only maintaining IP addresses of the servers. At scale, servers fail more frequently than expected. Along with that, with orchestration tools like Kubernetes pods are ephemeral, due to autoscaling, they keep on getting added or removed.
    * 3 Common ways of doing service discovery:
        1. Central service registry
        2. Traditional load balancer based registry
        3. Service mesh: Technologies like istio, consult. Also helps reduce the extra network due to load balancer.
    * If we don't do efficient service discovery, then it will increase the overall latency.

4. Authentication and Authorization between services
    * It's very crucial to have authentication and authorization for internal services.
    * Eg. someone in the org could misuse a service by bombarding it with messages.
    * It ensures that no service abuses another service either intentionally or accidentally.
    * We can have a central auth (internal service) issuing JWT tokens if we want to have a no trust policy.
    * Or we can add secrets for basic auth.

5. Configuration Management
    * Each service has its own set of secrets and configurations.
    * There needs to be a way to store these configurations centrally.
    * Every service doing configuration management on its own is a waste of time.

6. There's no going back (more of an organizational challenge)
    * It's very difficult to switch back to monolith from microservice. Why:
        * Tech diversity: going back to an old tech stack.
        * Teams have tasted autonomy.
        * People have adopted new tools and processes.

7. Fault tolerance
    * Since there are more components, there are more ways to fail.
    * Outages are inevitable but it is important that outage in one service is not bringing the entire system down.
    * Hence try to model services around: 
        * Loose coupling.
        * Asynchronous dependency.

8. Internal and External testing
    * Testing becomes super complex in case of microservices.
    * Running end to end test suites would require spinning up N servers for all N microservices which increase a lot of infra provisioning and cost.
    * It is very hard to simulate distributed failures.

9. Design with failure in mind
    * Assume that each line of code can file.
    * This will help in improving the error handling and also using patterns like circuit breaking so that we do not overwhelm the dependent service having network failures.

10. Dependency management is a nightmare
    * There are 3 dependencies to think about:
    
    1. Service Dependency: Sync dependency may trigger cascading failures.
    2. Library / Module dependency: 
        * Without proper versioning or backward compatibility, rolling out changes becomes painfully slow.'
        * We have to ensure proper versioning, else it would be a bigger pain. We have to also ensure that they are backward compatible.
    3. Data dependency:
        * Imagine the structure of data changing that is sent by the dependent service.