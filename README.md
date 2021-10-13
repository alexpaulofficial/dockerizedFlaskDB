# DockerizedFlaskDB

*Thesis for the exam "Electronic Computers and Networks", UNIVPM*

DockerizedFlaskDB is a collection of two projects that let interact a Python [Flask](https://flask.palletsprojects.com/en/2.0.x/) application with a database ([MySQL](https://www.mysql.com/) or [PostgreSQL](https://www.postgresql.org/)) in a Dockerized environment. The Flask app and the DB are into two different containers that are linked together with [Docker-Compose](https://docs.docker.com/compose/). The Flask app consists in a REST API that through the [routes](#application-routes) let you:

- Get all the students from the DB
- Add a student in the DB
- Remove a student with a certain id in the DB
- Remove all the students in the DB


# Table of contents

- [DB Model (Student)](#db-model-student)
- [Application Routes](#application-routes)
- [Differences between the two sub-projects](#differences-between-the-two-sub-projects)
- [Wiki](https://github.com/alexpaulofficial/dockerizedFlaskDB/wiki)

# DB Model (Student)

The DB has only one table of students (empty at the beginning). Each student has these parameters:

```sql
`id` int unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `city` varchar(50) NOT NULL,
  `address` varchar(200) NOT NULL,
  PRIMARY KEY (`id`)
```

# Application Routes
All the routes start from this address:  http://localhost:5000 (the port 5000 is the one used by Flask)

> **GET** /

It returns a JSON with all the students in the DB

> **POST** /student

It adds a student in the DB from a JSON given in the body request with this format:

```json
{
    "name": "string",
    "city": "string",
    "address": "string"
}
```

> **GET**  /deleteAll

It deletes all the students in the DB (with a TRUNCATE query)

> **POST** /studentDelete

It deletes the student in the DB with the "id" given in the body of the request with this JSON format:

```json
{
    "id": int
}
```
If the given id doesn't exist, the response will be "ID incorrect"

# Differences between the two sub-projects

You can read the comparison between PostgreSQL and MySQL in the [Wiki](https://github.com/alexpaulofficial/dockerizedFlaskDB/wiki/MySQL-vs-PostgreSQL). For this project with a small DB the choise is indifferent. The real differences in my projects are the way how the DB is created and the way a student is added in the DB. In fact in the MySQL sub-project the DB is created from the file "projcer.sql" (into the folder db) when the container is built and every student is inserted into the database writing the SQL query manually. In the other sub-project (PostgreSQL) the DB creation and the student addition is made automatically by [SQLAlchemy](https://www.sqlalchemy.org/), thanks to the class students that is a db.Model.