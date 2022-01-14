import sqlite3


# функция проверяет есть ли данное имя в бд и возвращает True или False
def player_exists(player_name):
    con = sqlite3.connect('little_carrot.db')
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
    con = sqlite3.connect('little_carrot.db')
    cur = con.cursor()
    level, map, health = 0, 1, 5

    try:
        cur.execute(f"INSERT OR IGNORE INTO users(player_name, level, map, health) "
                    f"VALUES('{player_name}',{level} , {map}, {health});")
    finally:
        con.commit()
        cur.close()
        con.close()


def get_current_hp():
    con = sqlite3.connect('little_carrot.db')
    cur = con.cursor()
    player_name = get_player_name()

    try:
        cur.execute(f"SELECT health FROM users WHERE player_name = '{player_name}'")
        return cur.fetchone()[0]
    finally:
        cur.close()
        con.close()


def set_hp(count_of_add_hp):
    con = sqlite3.connect('little_carrot.db')
    cur = con.cursor()
    player_name = get_player_name()

    try:
        cur.execute( f"UPDATE users SET health = {count_of_add_hp} "
                     f"WHERE player_name = '{player_name}'")
    finally:
        con.commit()
        cur.close()
        con.close()


def add_hp(count_of_add_hp):
    con = sqlite3.connect('little_carrot.db')
    cur = con.cursor()
    player_name = get_player_name()

    try:
        cur.execute(f"UPDATE users SET health = {count_of_add_hp + get_current_hp()} "
                    f"WHERE player_name = '{player_name}'")
    finally:
        con.commit()
        cur.close()
        con.close()


def damage_hp(count_of_damage_hp):
    con = sqlite3.connect('little_carrot.db')
    cur = con.cursor()
    player_name = get_player_name()

    try:
        cur.execute( f"UPDATE users SET health = {get_current_hp() - count_of_damage_hp} "
                     f"WHERE player_name = '{player_name}'")
    finally:
        con.commit()
        cur.close()
        con.close()


def save_level(level):
    con = sqlite3.connect('little_carrot.db')
    cur = con.cursor()
    player_name = get_player_name()

    try:
        cur.execute( f"UPDATE users SET level = {level} "
                     f"WHERE player_name = '{player_name}'")
    finally:
        con.commit()
        cur.close()
        con.close()


def get_level():
    con = sqlite3.connect('little_carrot.db')
    cur = con.cursor()
    player_name = get_player_name()

    try:
        cur.execute(f"SELECT level FROM users WHERE player_name = '{player_name}'")
        return cur.fetchone()[0]
    finally:
        cur.close()
        con.close()


def reset_player():
    con = sqlite3.connect('little_carrot.db')
    cur = con.cursor()
    player_name = get_player_name()

    try:
        cur.execute(f"UPDATE users SET health = 5 "
                    f"WHERE player_name = '{player_name}'")

        cur.execute(f"UPDATE users SET level = 0 "
                    f"WHERE player_name = '{player_name}'")
    finally:
        con.commit()
        cur.close()
        con.close()


def get_player_name():
    with open("data/qt/current_player.txt", 'r', encoding='utf-8') as file:
        player_name = file.read().split()[0]
    return player_name
