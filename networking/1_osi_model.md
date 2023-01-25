* Open Systems Interconnection Model
* Every machine in the n/w has an IP address and MAC address assigned to it.

**Layer 7 Application Layer**
GET / 10.0.0.3 80
HTTP headers, cookies, content-type, etc. 

**Layer 6 Presentation Layer**
* Enrcypt if necessary. (if we use HTTPS/TLS)

**Layer 5 Session Layer**
* Stateful part.
* The data will be tagged to a session id.

**Layer 4 Transport Layer**
* This layer sees the data in bits.
* It breaks the data into segments.
* A source port and a destination port is tagged to each segment.
* Source port is auto-generated.
* The segments are maitained in sorted order.

**Layer**