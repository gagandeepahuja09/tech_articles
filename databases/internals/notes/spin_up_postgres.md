* docker run -e POSTGRES_PASSWORD=postgres --name pg1 postgres.
* No need to expose the port as we'll ssh into the container.

* docker exec -it pg1 psql -U postgres
    * create table temp(t int);

* create table temp(t int);
* insert into temp(t) select random()*100 from generate_series(0, 1000000);