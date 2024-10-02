import mysql.connector

conn = mysql.connector.connect(
    host='localhost',
    user='root',
    password='2211',
    database='chatbot_db'
)

cursor = conn.cursor()

# Insert a row of data
cursor.execute("INSERT INTO users (name, info) VALUES (%s, %s)", ('Alice', 'Likes books'))
conn.commit()

cursor.close()
conn.close()
