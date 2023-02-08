import readline
from collections import defaultdict

class ValueCountingDB:
    ## This class is a building block for ValueCountingDBWithTransactions. An
    ## instance of ValueCountingDB represents one transaction in a stack of open
    ## transactions.
    ##
    ## For simplicity, we `delete` keys by setting them to `None`. This
    ## enables a deleted key in this transaction to shadow any previous values
    ## they key may have in earlier transactions.
    def __init__(self):
        self.db = {}
        self.counter = defaultdict(int)

    def get(self, key):
        return self.db[key] if key in self.db else None

    def set(self, key, val, old_val):
        # We only update the counter if old_val is not None. This must be
        # provided as an argument because we don't have access to other
        # transactions here.
        if old_val:
            self.counter[old_val] -= 1
        self.counter[val] += 1
        self.db[key] = val

    def delete(self, key, old_val):
        # We only update the counter if old_val is not None. This must be
        # provided as an argument because we don't have access to other
        # transactions here.
        self.db[key] = None
        if old_val:
            self.counter[old_val] -= 1

    def count(self, val):
        return self.counter[val]

class ValueCountingDBWithTransactions:
    def __init__(self):
        self.transactions = [ValueCountingDB()]

    def _get(self, key):
        for i in range(len(self.transactions)-1, -1, -1):
            if key in self.transactions[i].db:
                return self.transactions[i].get(key)

    def get(self, key):
        return self._get(key) or 'NULL'

    def set(self, key, val):
        self.transactions[-1].set(key, val, self._get(key))

    def delete(self, key):
        self.transactions[-1].delete(key, self._get(key))

    def count(self, val):
        return sum([trx.count(val) for trx in self.transactions])

    def begin(self):
        self.transactions.append(ValueCountingDB())

    def rollback(self):
        if len(self.transactions) > 1:
            self.transactions.pop()

    def commit(self):
        # When we commit, we merge the database in each transaction into the
        # root, including deletes. This means that over time we will
        # accumulate unnecessary deleted entries, but we could easily amortize
        # the cost of cleanup.
        [root, *rest] = self.transactions
        for trx in rest:
            for (key, val) in trx.db.items():
                root.set(key, val, root.get(key))
        self.transactions = [root]

    def report(self):
        for trx in self.transactions:
            print("trx", trx.db, sorted(list(trx.counter.items())))

db = ValueCountingDBWithTransactions()
while True:
    [command, *args] = input('>> ').split()
    command = command.upper()
    if command == "END":
        print()
        break
    elif command == "SET":
        db.set(*args)
    elif command == "GET":
        print(db.get(*args) or 'NULL')
    elif command == "DELETE":
        db.delete(*args)
    elif command == "COUNT":
        print(db.count(*args))
    elif command == "BEGIN":
        db.begin()
    elif command == "ROLLBACK":
        db.rollback()
    elif command == "COMMIT":
        db.commit()
    elif command == "REPORT":
        db.report()
    else:
        print("Unknown command")
