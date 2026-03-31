from db.database import get_cursor

def get_setting_by_id(id):
    conn, cur = get_cursor()
    cur.execute("SELECT * FROM circle_settings WHERE id = %s", (id,))
    row = cur.fetchone()
    cur.close()
    conn.close()
    return row