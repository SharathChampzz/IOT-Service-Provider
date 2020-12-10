import sqlite3


def adduser(projectname, path, url, sendbackdata):
	conn = sqlite3.connect('mysqlite.db')
	c = conn.cursor()
	c.execute('''CREATE TABLE IF NOT EXISTS monitor
	             (projectname text, jsonpath text, url text, firebasetomcu text)''')
	if not geturl(path):
		c.execute('''INSERT INTO monitor (projectname, jsonpath, url, firebasetomcu) values (?,?,?,?)''', (projectname, path, url, sendbackdata))
	conn.commit()
	conn.close()

def getusers():
	try:
		conn = sqlite3.connect('mysqlite.db')
		c = conn.cursor()
		c.execute('SELECT * FROM monitor')
		rows = c.fetchall()
		conn.commit()
		conn.close()
		# print(rows)
		return rows
	except Exception as e:
		print(e)
		return []

def getfirebasetomcu(projectname):
	try:
		conn = sqlite3.connect('mysqlite.db')
		c = conn.cursor()
		cmd = 'SELECT firebasetomcu FROM monitor WHERE projectname = ?'
		c.execute(cmd,(projectname, ))
		row = c.fetchone()
		conn.commit()
		conn.close()
		if row is None:
			return "Get Firebase to MCU is Empty"
		else:
			return row[0]
	except Exception as e:
		print(e)
		return "Error while : Get Firebase to MCU"


def geturl(jsonid):
	try:
		conn = sqlite3.connect('mysqlite.db')
		c = conn.cursor()
		cmd = 'SELECT url FROM monitor WHERE jsonpath = ?'
		c.execute(cmd,(jsonid, ))
		row = c.fetchone()
		conn.commit()
		conn.close()
		if row is None:
			return False
		else:
			return row[0]
	except Exception as e:
		print(e)
		return False

def clear():
	conn = sqlite3.connect('mysqlite.db')
	c = conn.cursor()
	c.execute('''DELETE FROM MONITOR''')
	conn.commit()
	conn.close()

def updatefirebasetomcu(projectname, data):
	try:
		conn = sqlite3.connect('mysqlite.db')
		c = conn.cursor()
		cmd = 'UPDATE monitor SET firebasetomcu = ? WHERE projectname = ?'
		c.execute(cmd,(data, projectname))
		conn.commit()
		conn.close()
	except Exception as e:
		print(e)


# updatefirebasetomcu('fyp-healthapp-project', 'send this data to MCU')
# # adduser('projectname', 'efgh','fttp', 'firebasetomcu')
print(getusers())
# print(getfirebasetomcu('projectname'))
# clear()
# print(getusers())



# res = geturl('efgh')
# if res:
# 	print(res)
# else:
# 	print('User Not Found!')
