=======
Quijibo
=======

*Dude, that's not how you spell "kwijibo"*

Quijibo - it has a "Q" and a "J", and so a good name for a JSON to SQL
translation layer. Yes, you build a JavaScript object that mirrors a
query tree, serialize it to JSON, and Quijibo will take your JSON and translate
it to SQL via SQLAlchemy.

Wait, web clients can execute SQL?
==================================

No, not really. They can build query trees using JavaScript objects that will
be safely translated to a limited subset of SQL.

What SQL dialects are supported?
================================

PostgreSQL.

What kinds of queries can you do?
=================================

Because the JSON objects mirror the structure of SQLAlchemy Expression
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

It is planned to continue extending the capabilities of Quijibo as the
demand arises, but with only "safe" constructs possible.

A "dangerous" add-on is planned, for the cases where you can ensure an
authenticated client is mapped to a database user with strictly defined
privileges.

