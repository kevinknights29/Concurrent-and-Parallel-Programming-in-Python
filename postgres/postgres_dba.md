# Commands to Adminisitrate a Postgres Database

## Connecting to the Database

To connect to a PostgreSQL database from the container's command line:

```sh
psql -U postgres -d postgres
```

## Listing Tables

The `\z` command is a good way to list tables when inside the interactive psql session.

```sh
\z
```

Alternatively, you can use:

```sh
\dt
```

## Listing Databases

To list all databases:

```sh
\l
```

## Creating a New Database

To create a new database:

```sh
CREATE DATABASE dbname;
```

## Deleting a Database

To delete a database:

```sh
DROP DATABASE dbname;
```

## Creating a New User

To create a new user:

```sh
CREATE USER username WITH PASSWORD 'password';
```

## Granting Privileges

To grant all privileges on a database to a user:

```sh
GRANT ALL PRIVILEGES ON DATABASE dbname TO username;
```

## Listing Users

To list all users:

```sh
\du
```

## Changing a User's Password

To change a user's password:

```sh
ALTER USER username WITH PASSWORD 'newpassword';
```

## Viewing Table Structure

To view the structure of a table:

```sh
\d tablename
```

## Inserting Data

To insert data into a table:

```sh
INSERT INTO tablename (column1, column2) VALUES (value1, value2);
```

## Updating Data

To update data in a table:

```sh
UPDATE tablename SET column1 = value1 WHERE condition;
```

## Deleting Data

To delete data from a table:

```sh
DELETE FROM tablename WHERE condition;
```

## Backing Up a Database

To back up a database:

```sh
pg_dump dbname > backupfile.sql
```

## Restoring a Database

To restore a database from a backup:

```sh
psql dbname < backupfile.sql
```

## Checking Database Size

To check the size of a database:

```sh
SELECT pg_size_pretty(pg_database_size('dbname'));
```

## Exiting the psql Session

To exit the interactive psql session:

```sh
\q
```
