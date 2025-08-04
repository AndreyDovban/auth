# Функция создание таблицы пользователей
# @param {Object} cur Объект соединение с базой
# @return {void}
def create_users(cur):
    cur.execute('''CREATE TABLE IF NOT EXISTS users(
                uuid TEXT PRIMARY KEY,
                name TEXT,
                description TEXT,
                role TEXT,
                password TEXT
                )'''
                )
    pass
