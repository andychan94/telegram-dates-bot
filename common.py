from enum import Enum

import mysql.connector

from settings import conf, messages


def db_worker(operation, *args):
    cursor = None
    queries = {
        'get_state': "SELECT state FROM user_state WHERE id=%s",
        'insert_new_state': "INSERT INTO user_state (id, state) VALUES(%s, '" + States.S_START.value + "')",
        'update_state': "UPDATE user_state SET state=%s WHERE id=%s",
        'update_state_date_id': "UPDATE user_state SET state=%s, current_date_id=%s WHERE id=%s",
        'insert_name': "INSERT INTO group_dates (name) VALUES (%s)",
        'get_current_date_id': "SELECT current_date_id FROM user_state WHERE id=%s",
        'set_type': "UPDATE group_dates SET date_type=%s WHERE id=%s",
        'set_date': "UPDATE group_dates SET date=%s WHERE id=%s",
        'set_photo_path': "UPDATE group_dates SET img_path=%s WHERE id=%s",
        'get_one_date': "SELECT name, date_type, DATE_FORMAT(date, '%D %M, %Y'), img_path FROM group_dates WHERE id=%s",
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
            inserted_id = cursor.lastrowid
            ctn.commit()
            return inserted_id
        elif operation == 'update_state_date_id':
            cursor.execute(queries['update_state_date_id'], args)
            ctn.commit()
            return operation
        elif operation == 'get_current_date_id':
            cursor.execute(queries['get_current_date_id'], args)
            result = cursor.fetchone()
            return int(result[0])
        elif operation == 'set_type':
            cursor.execute(queries['set_type'], args)
            ctn.commit()
            return operation
        elif operation == 'set_date':
            cursor.execute(queries['set_date'], args)
            ctn.commit()
            return operation
        elif operation == 'set_photo_path':
            cursor.execute(queries['set_photo_path'], args)
            ctn.commit()
            return operation
        elif operation == 'get_one_date':
            cursor.execute(queries['get_one_date'], args)
            result = cursor.fetchone()
            return result
    finally:
        cursor.close()
        ctn.close()


def verify_user_valid(chat_id, bot):
    if int(chat_id) != int(conf['user_id']):
        bot.send_message(chat_id, messages['not_valid_user'])
        return False
    return True


class States(Enum):
    S_START = 'new'
