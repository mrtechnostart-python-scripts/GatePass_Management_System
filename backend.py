import hashlib
import sqlite3
conn = sqlite3.connect("users.db")
c = conn.cursor()
admin = sqlite3.connect("watchman.db")
ac = admin.cursor()

def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False


def addUser(username,password):
    c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')
    c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
    conn.commit()

def watchMan(username,password):
	ac.execute('CREATE TABLE IF NOT EXISTS watchManTable(username TEXT,password TEXT)')
	ac.execute('INSERT INTO watchManTable(username,password) VALUES (?,?)',(username,password))
	admin.commit()



def inputUserData():
	username = input("Enter Student Name ")
	password = input("Enter Password")
	hashed_passwd = make_hashes(password)
	addUser(username,hashed_passwd)

def inputWatchManData():
	username = input("Enter WatchMen Name")
	password = input("Enter Password")
	hashed_passwd = make_hashes(password)
	watchMan(username,hashed_passwd)
userChoice = int(input("Press 1 For Creating User and 2 for watchman"))
if userChoice == 1:
	inputUserData()
elif userChoice == 2:
	inputWatchManData()
	

