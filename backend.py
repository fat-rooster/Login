from Utilities.Db_utilities import get_db, get_user_id
import uuid




def get_password_for_user(user_id):
    conn =get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT password FROM users WHERE user_id = ?", (user_id, ))
    result = cursor.fetchone()
    if result:
        print(result['password'])
        return result['password']
    else:
        print('user not found')
        return None

def create_user(user_name, password):
    conn=get_db()
    if get_user_id(user_name): return
    user_id = str(uuid.uuid4())
    try:
        conn.execute('BEGIN TRANSACTION')
        conn.execute('INSERT INTO entities(entity_id, table_index) VALUES (?, ?)', (user_id, 0))
        conn.execute('INSERT INTO users(user_name, user_id, password) VALUES (?, ?, ?)', (user_name, user_id, password))
        conn.commit()
    except:
        conn.rollback()
        raise

def name_available(user_name):
    return True

def password_acceptor(password):
    return True

def hash(x):
    return x

def check_password(user, password):
    target = get_password_for_user(user.id)
    if hash(password) == target:
        return True
    return False

