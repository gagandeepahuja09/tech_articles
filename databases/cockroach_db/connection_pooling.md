* https://www.cockroachlabs.com/blog/what-is-connection-pooling/

**A Typical Database Connection**

* *Steps*
    1. The application uses a *database driver* to *open a connection*.
    2. A *network socket is opened* to connect the application and the database.
    3. The user is *authenticated*.
    4. The operation completes and the application can be closed.
    5. The *network socket is closed*.
* Not consuming the resources and keeping it ideal also consumes resources.

**Why pool database connections?**
* At scale, the constant opening and closing of connections becomes more expensive and can impact our application's performance.
* We maintain a pool of open connections that can be passed from database operation to database operation as needed.
* We need not build a connection pool from ground up: eg pgxpool.
* *We want to size our connection pool such that the number of idle connections is minimized, but so if the frequency with which we have to open/close new connections.*
* We also want to be sure that the *maximum no. of connections is appropriate as this reflects the max work our database can do*.