import sqlite3 



try:
    db = sqlite3.connect('New.db')

    cur = db.cursor() 
    cur.execute('CREATE TABLE IF NOT EXISTS tasks (ID INTEGER PRIMARY KEY, Task VARCHAR(255) NOT NULL, Date VARCHAR(255) NOT NULL)')
    
except Exception as e:
    print(e)

