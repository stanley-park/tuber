import sqlite3

conn = sqlite3.connect('Tuber_DB_A.db')
c = conn.cursor()

def create_table():
    c.execute('CREATE TABLE IF NOT EXISTS Student(s_name TEXT, s_classkey TEXT, s_ckey REAL,s_radius REAL, s_key REAL)')

def data_entry():
    c.execute("INSERT INTO Student (s_name,s_classkey,s_ckey,s_radius, s_key) VALUES('Mark', 'CSE_20', 0002, 1, 0021)")
    conn.commit()
    c.close()
    conn.close()
    
create_table()
data_entry()