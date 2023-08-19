from flask import Blueprint
from Utilities.Db_utilities import table_ids
from sqlite3 import Error

def create_users_table(i, conn):
    
    try:
        sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                        user_name TEXT,
                                        user_id TEXT PRIMARY KEY,
                                        password TEXT,
                                        FOREIGN KEY (user_id) REFERENCES entities(entity_id) ON DELETE CASCADE
                                    ); """
        if conn is not None:
            conn.execute(sql_create_users_table)
            conn.execute('CREATE UNIQUE INDEX IF NOT EXISTS idx_username ON users(user_name)')
        else:
            print("Error! could not create users table")
    except Error as e:
        print(e)
    conn.execute('INSERT OR IGNORE INTO tables(table_index, table_name) VALUES (?,?)', (i, 'users'))
    conn.commit()
    table_ids.users=i



login = Blueprint('Login', __name__)

from . import routes