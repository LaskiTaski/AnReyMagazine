import sqlite3 as sq


def sql_start_client():
    global base, cur
    base = sq.connect('magazine.dp')
    cur = base.cursor()
    if base:
        base.execute('CREATE TABLE IF NOT EXISTS information_base('
                     'Name INTEGER ,'
                     'URL INTEGER ,'
                     'course INTEGER ,'
                     'FullPrice INTEGER ,'
                     'NumOfPos INTEGER ,'
                     'Result INTEGER )'
                     )
        print('Клиентская база запущенна')
    base.commit()


async def sql_add_command_client(state):
    async with state.proxy() as data:
        cur.execute('INSERT OR IGNORE INTO information_base VALUES (?, ?, ?, ?, ?, ?)', tuple(data.values())[1::])
        base.commit()


def sql_read_command_client():
    try:
        cursor = base.cursor()

        sqlite_select_query = 'SELECT * from settings'
        cursor.execute(sqlite_select_query)
        records = cursor.fetchall()
        return records

    except sq.Error as error:
        print("Ошибка при работе с SQLite", error)