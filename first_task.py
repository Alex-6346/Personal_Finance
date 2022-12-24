from splitwise import Splitwise
import sqlite3
from sqlite3 import Error

from sql_queries_methods import create_tables, fill_tables


def access_to_splitwise():
    s_obj = Splitwise("jYKW9NrdaDToz0Yozc3R6bS0yoQ0BEABc4JhFXEh", "hGJPvIbnuufdVMSIqnk8UBoz7JhudYyutZtweGeh",
                      api_key="GalhmollL6o1lGlcRDY2XXsUVZkhgdKqcbX65DMY")
    return s_obj


def splitwise_sync(s_obj: Splitwise):
    user = s_obj.getCurrentUser()
    user_id = user.getId()
    conn = None
    cursor = None
    try:
        conn = sqlite3.connect(str(user_id) + ".sqlite")
        cursor = conn.cursor()
    except Error as e:
        print(e)

    # TODO: Exception handling
    create_tables(cursor)
    fill_tables(s_obj, cursor)
    conn.commit()
    conn.close()


if __name__ == '__main__':
    sObj = access_to_splitwise()
    splitwise_sync(sObj)
