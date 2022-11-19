**Common Linux Signals: SIGTERM, SIGINT, SIGKILL**

*What is a linux signal*
* Just like a traffic signal, it is a way of the linux OS signalling something to the running program.
* These are mapped to a number b/w 1-30+.
    * SIGTERM: 15
    * SIGKILL: 9
* SIGTERM: Just like a red-light signal, it sends a signal asking the program to be terminate it. The program may ignore. The common purpose of these signals is to inform the program so that it can handle graceful termination. Eg:
    * Not allowing new users to connect.
    * Terminating connections with the existing users.
    * Completing inflight DB requests.
* SIGKILL: It is used to forcefully terminate a program eg: when it is hanging.

* SIGTERM and SIGKILL are more general purpose while SIGINT is termination requested by the client or user from termination generally via ctrl+C.