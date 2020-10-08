import mysql.connector
from settings import conf, constants
from enum import Enum


def db_worker(operation, *args):
    cursor = None
    queries = {
        'get_state': "SELECT state FROM user_state WHERE id=%s",
        'insert_new_state': "INSERT INTO user_state (id, state) VALUES(%s, '" + States.S_START.value + "')",
        'update_state': "UPDATE user_state SET state=%s WHERE id=%s",
        'insert_name': "INSERT INTO group_dates (name) VALUES (%s)",
    }
    ctn = mysql.connector.connect(**conf['mysql'])
    try:
        cursor = ctn.cursor()
        if operation == 'get_state':
            cursor.execute(queries['get_state'], args)
            result = cursor.fetchone()
            if result is None:
                cursor.execute(queries['insert_new_state'], args)
                ctn.commit()
                return 'new'
            return str(result[0])
        elif operation == 'update_state':
            cursor.execute(queries['update_state'], args)
            ctn.commit()
            return operation
        elif operation == 'insert_name':
            cursor.execute(queries['insert_name'], args)
            ctn.commit()
            return operation
    finally:
        cursor.close()
        ctn.close()


def verify_user_valid(chat_id, bot):
    if int(chat_id) != int(conf['user_id']):
        bot.send_message(chat_id, constants['not_valid_user'])
        return False
    return True


class States(Enum):
    S_START = 'new'
