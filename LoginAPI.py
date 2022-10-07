import psycopg2
import hashlib


hash = (hashlib.sha256('Mostafa123'.encode())).hexdigest()
username = 'mostafa'
conn = psycopg2.connect(
   database="Daraya1", user='postgres', password='Daraya123', host='localhost', port= '5432'
)
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS useraccount")

sql ='''CREATE TABLE useraccount(
	username VARCHAR ( 100 ) NOT NULL,
	password VARCHAR ( 100 ) NOT NULL

)'''
cursor.execute(sql)
print("Table created successfully")
conn.commit()

conn.autocommit = True

cursor = conn.cursor()

sql = ''' DELETE FROM useraccount '''
cursor.execute(sql)
conn.commit()
cursor.execute("INSERT INTO useraccount(username, password) VALUES (%s,%s)",(username,hash))

conn.close()