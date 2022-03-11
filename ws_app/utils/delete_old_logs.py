import time
import psycopg2

def clear_old_logs():
    conn = psycopg2.connect(
        host="192.168.42.134",
        database="authlog",
        user="authlogowner",
        password="UTyt0Dk9HNXz6H61ekMQ")
    cur = conn.cursor()
    controltime = int(time.time()) - 8640000 # 100 дней
    d = """ delete from authlog where datetime < """+str(controltime)
    cur.execute(d)
    conn.commit()
