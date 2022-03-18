import sqlite3


conn = sqlite3.connect('../../data/little_carrot.db')
cur = conn.cursor()

#create users table and fill data
cur.execute("""CREATE TABLE IF NOT EXISTS users(
   user_id INTEGER PRIMARY KEY AUTOINCREMENT,
   player_name TEXT,
   level INT,
   map INT,
   health INT);
""")

cur.execute("""INSERT INTO users(player_name, level, map, health)
   VALUES('Anna', 1, 1, 0);""")

cur.execute("""INSERT INTO users(player_name, level, map, health)
   VALUES('Arthur', 1, 1, 0);""")

cur.execute("""INSERT INTO users(player_name, level, map, health)
   VALUES('Aleksey', 1, 1, 0);""")

conn.commit()
