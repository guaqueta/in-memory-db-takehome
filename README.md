# In-memory Database

I provide two implementations

## Keeping count with Python

The `db.py` file can be run with python3. With no arguments it provides an
interactive prompt to run database commands. On a shell you can also stream a
file of commands to it (one per line) by running `python3 db.py < filename`.

In the python implementation we maintain two hash-maps: one for the database
values, and one for the counts. Transactions are implemented as a stack of
databases, with more recent transactions shadowing older ones. `SET`, `GET`,
`DELETE`, and `COUNT` are O(m) (where m is the number of open
transactions). `BEGIN` and `ROLLBACK` are O(1), and `COMMIT` is O(m k), where
m is the number of open transactions and k is the number of affected keys per
transaction.

## Being lazy with Clojure

To run the clojure implementation you can:
1. [Install the clojure command-line tools](https://clojure.org/guides/install_clojure). With `db.clj` and `deps.edn` in your directory you can then run `clojure -M db.clj`.
2. [Use this replit](https://replit.com/@turingcomplete/DevotedDB#main.clj). I uploaded my solution to a repl.it so that you can run it in the browser. It's slow, but doesn't require any installation.

The clojure implementation uses a library that implements a hash-map sorted by
values. This `priority-map` data structure provides O(log n)-or-better `GET`,
`SET`, `DELETE`, and `COUNT`. For transactions we rely on clojure's immutable
data structures. Opening a new transaction is as simple as hanging on to a
reference to the current database value. `BEGIN`, `ROLLBACK`, and `COMMIT` are
all O(1), since they are just changing the current reference to the
database. I couldn't resist implementing the clojure solution since all the
hard work is already done for me.
