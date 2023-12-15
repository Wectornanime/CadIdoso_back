import sqlite3

db = sqlite3.connect('database.db')
cmd = "SELECT * FROM idosos"
mycursor = db.cursor()

res = mycursor.execute(cmd).fetchall()

print(res)