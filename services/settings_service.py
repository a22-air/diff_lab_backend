from db.database import get_cursor

def save_setting(data):
    conn, cur = get_cursor()

    cur.execute("""
        INSERT INTO circle_settings (count, radius, ring_radius, color)
        VALUES (%s, %s, %s, %s)
    """, (data.count, data.radius, data.ringRadius, data.color))

    conn.commit()
    cur.close()
    conn.close()


def get_settings():
    conn, cur = get_cursor()

    cur.execute("SELECT * FROM circle_settings ORDER BY id DESC")
    rows = cur.fetchall()

    cur.close()
    conn.close()

    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "count": row[1],
            "radius": row[2],
            "ring_radius": row[3],
            "color": row[4],
            "created_at": str(row[5])
        })

    return result


def delete_setting(id):
    conn, cur = get_cursor()

    cur.execute("DELETE FROM circle_settings WHERE id = %s", (id,))
    conn.commit()

    cur.close()
    conn.close()


def update_setting(id, data):
    conn, cur = get_cursor()

    cur.execute("""
        UPDATE circle_settings
        SET count = %s, radius = %s, ring_radius = %s, color = %s
        WHERE id = %s
    """, (data.count, data.radius, data.ringRadius, data.color, id))

    conn.commit()
    cur.close()
    conn.close()