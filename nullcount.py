import sqlite3

conn = sqlite3.connect('testing0.db',isolation_level=None)
c = conn.cursor()

# null values
# 4	5	6	4
# 8	9	10	4
# 8	9	10	5


c.execute("SELECT COUNT(*) FROM table0")
for row in c:
    print(row)

    # count is 4


c.execute("SELECT COUNT(colA) FROM table0")
for row in c:
    print(row)

    # count is 3


c.execute("SELECT (colA) FROM table0")
for row in c:
    print(row)

# (None,)
# ('4',)
# ('8',)
# ('8',)

s = "some bs \"~\""
print(s)

