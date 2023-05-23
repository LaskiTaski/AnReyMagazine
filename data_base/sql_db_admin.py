import sqlite3 as sq


def sql_start_admin():
    global base, cur
    base = sq.connect('magazine.dp')
    cur = base.cursor()
    if base:
        base.execute('CREATE TABLE IF NOT EXISTS settings('
                     'id INTEGER PRIMARY KEY AUTOINCREMENT,'
                     'Delivery INTEGER ,'
                     'Guarantee INTEGER ,'
                     'Commission INTEGER )'
                     )
        print('Админская база запущенна')
    base.commit()


async def sql_add_command_admin(state):
    async with state.proxy() as data:
        cur.execute('INSERT OR IGNORE INTO settings VALUES (?, ?, ?, ?)', tuple(data.values()))
        base.commit()


async def sql_update_command_admin(key,value):
    try:
        cursor = base.cursor()

        if key == 'Delivery':
            sql_request = 'UPDATE settings set Delivery = ? WHERE id = 1'
        elif key == 'Guarantee':
            sql_request = 'UPDATE settings set Guarantee = ? WHERE id = 1'
        else:
            sql_request = 'UPDATE settings set Commission = ? WHERE id = 1'
        data = (value,)
        cursor.execute(sql_request, data)
        base.commit()
        print("Запись успешно обновлена")

    except sq.Error as error:
        print("Ошибка при работе с SQLite", error)

def sql_read_command_admin():
    try:
        cursor = base.cursor()

        sqlite_select_query = 'SELECT * from settings'
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        return records

    except sq.Error as error:
        print("Ошибка при работе с SQLite", error)