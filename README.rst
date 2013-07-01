====================
qjb-qexec-sqlalchemy
====================

`quijibo`_ Query Executor for `SQL Alchemy`_. Given an `SQL Alchemy`_ `Table`_
to be queried, this Executor interprets `quijibo`_ Query Trees and constructs
an `SQL Alchemy`_ query, optionally executing it immediately.

.. _SQL Alchemy: http://www.sqlalchemy.org/

.. _Table: http://docs.sqlalchemy.org/en/latest/core/schema.html#sqlalchemy.schema.Table

.. _quijibo: https://github.com/sprin/quijibo

The typical use case is executing a JSON-serialized `quijibo`_ Query Tree that
has been received in the form of an AJAX request.

Wait, web clients can execute SQL?
==================================

No, not really. They can build Query Trees using JavaScript objects that will
be safely translated to a limited subset of SQL.

What SQL dialects are supported?
================================

PostgreSQL.

What kinds of queries can you do?
=================================

Because the JSON objects mirror the structure of `SQL Alchemy`_ Expression
Language queries, which mirror the structure of the query tree (the result of
parsing the SQL statement), it is theoretically possible for Quijibo to be able
execute any arbitrary query that Alchemy can. How much power you want to give
the client to query should be up to you, so it is planned to make the possible
query constructs highly configurable.

Watch this space
----------------

Currently, simple SELECTs on a single view or base table are possible. Most of
the current emphasis is on complex qualifications (WHERE). However, if you like
to just take the qualification and insert it anywhere in to a server-defined
query, you can do so.

It is planned to continue extending the capabilities of this Quijibo Query
Executor as the demand arises, but with only "safe" constructs possible.

A "dangerous" add-on is planned, for the cases where you can ensure an
authenticated client is mapped to a database user with strictly defined
privileges.

