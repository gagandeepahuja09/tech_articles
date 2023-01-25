* Each machine (machine/vm/container) has an IP address.
* There are 1000s of applications running on a machine. Port is used to give the differentiation of the application that is running.

Few Reserved Application Ports
* HTTP Server: 80
* SMTP: 25
* TELNET: 23
* SSH

**TCP**
* It is a communication protocol designed to send information from one server to another by specifying the IP address and the port.
* HTTP uses it underneath, Databases use TCP.

Pros:
* Acknowledgement
    * Network is unreliable.
    * If the client didn't receive the acknowledgement from the server, it doesn't trust that.
* Guaranteed Delivery
    * The client will send the information again if it doesn't receive the acknowledgement (retransmission).
    * The acknowledgment could come but it could be out of order.
* Connection Based
    * The client and server need to establish a connection b/w them.
    * The connection is stateful in nature. The process and the server hold information about the connection.
* Congestion Control
    * The packets could get delayed due to the routers getting overwhelmed.
    * Congestion control tries to avoid this.
* Ordered packets

Cons:
* Larger packets
    * We require headers for everything: ack, guaranteed delivery, congestion control.
* More bandwidth
* Slower than UDP
* Stateful