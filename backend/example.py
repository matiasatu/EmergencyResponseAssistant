import sqlite3

con = sqlite3.connect("test.db")
cur = con.cursor()


with open("../db/create.sql", "r") as f:
    script = f.read()
    cur.executescript(script)

cur.execute("INSERT INTO user VALUES(?,?,?)", ["ggarzia", "this is my bio", 6034568515])
con.commit()