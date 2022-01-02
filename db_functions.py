# функция проверяет есть ли данное имя в бд и возвращает True или False
def player_exists(player_name):
    con = sqlite3.connect('data/little_carrot.db')
    cur = con.cursor()

    try:
        cur.execute(f"SELECT count(*) FROM users WHERE player_name = '{player_name}'")
        value = cur.fetchone()
        if value[0] == 0:
            return False
        else:
            return True
    finally:
        cur.close()
        con.close()


# добавляет игрока в db
def add_player(player_name):
    con = sqlite3.connect('data/little_carrot.db')
    cur = con.cursor()
    level, map, health = 1, 1, 0

    try:
        cur.execute(f"INSERT OR IGNORE INTO users(player_name, level, map, health) "
                    f"VALUES('{player_name}',{level} , {map}, {health});")
    finally:
        con.commit()
        cur.close()
        con.close()

