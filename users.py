import sqlite3 
import streamlit as st
import pandas as pd
import hashlib
import random
import datetime
# Security
#passlib,hashlib,bcrypt,scrypt
def getDateTime():
	return [str(datetime.date.today()),str(datetime.datetime.now().strftime("%H:%M"))]
def getReturnTime():
	return [str(datetime.date.today()),str("22:00")]
def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def randomGenerator():
    a = random.sample(range(10),3)
    number = (str(random.randint(1,9)) + str(a[0]) + str(a[1]) + str(a[2]))
    return number

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False
# DB Management
conn = sqlite3.connect('users.db')
c = conn.cursor()


gatePass = sqlite3.connect('gatepass.db')
gate = gatePass.cursor()
gate.execute('CREATE TABLE IF NOT EXISTS marketPassTable(username TEXT,otp TEXT,datetime TEXT,expectedDateTime TEXT)')
# DB  Functions


def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data


def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data


def isapplied(username):
    gate.execute('SELECT datetime,expectedDateTime FROM marketPassTable WHERE username =?',(username,))
    data = gate.fetchall()
    if len(data) >= 1:
        return False
    return True

def applyPass(username,otp,dateTime,returnTime):
	gate.execute('INSERT INTO marketPassTable(username,otp,datetime,expectedDateTime) VALUES (?,?,?,?)',(username,otp,dateTime[0]+" "+dateTime[1],returnTime[0]+" "+returnTime[1]))
	gatePass.commit()
	st.success("Gate Pass Applied Successfully")
	st.success("Your OTP is {}".format(otp))


def applyHomePass(username,otp,dateTime,returnTime):
	gate.execute('INSERT INTO marketPassTable(username,otp,datetime,expectedDateTime) VALUES (?,?,?,?)',(username,otp,dateTime[0]+" "+dateTime[1],returnTime[0]+" "+returnTime[1]))
	gatePass.commit()
	st.success("Home Pass Applied Successfully")
	st.success("Your OTP is {}".format(otp))

def main():
	"""Simple Login App"""

	st.title("Student's GatePass Dashboard")

	menu = ["Home","Login"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Home":
		st.subheader("Home")

	elif choice == "Login":
		st.subheader("Login Section")

		username = st.sidebar.text_input("User Name")
		password = st.sidebar.text_input("Password",type='password')
		if st.sidebar.checkbox("Login"):
			# if password == '12345':
			hashed_pswd = make_hashes(password)

			result = login_user(username,check_hashes(password,hashed_pswd))
			if result:
				st.success("Logged in as {}".format(username))
				task = st.selectbox("Tasks",["Apply Gate Pass","Apply Home Pass"])
				if task == "Apply Gate Pass":
					otp = randomGenerator()
					dateTime = getDateTime()
					returnTime = getReturnTime()
					if st.button("Apply Now!"):
						if isapplied(username):
							applyPass(username,otp,dateTime,returnTime)
						else:
							gate.execute('SELECT otp FROM marketPassTable WHERE username =?',(username,))
							data = gate.fetchall()
							st.warning("Already Applied, Cancel First, OTP = {}".format(data[0][0]))
				elif task == "Apply Home Pass":
					otp = randomGenerator()
					dateTime = getDateTime()
					returnDate = str(st.date_input("Input Date"))
					returnTime = [returnDate,"22:00"]
					if st.button("Apply Now!"):
						if isapplied(username):
							applyHomePass(username,otp,dateTime,returnTime)
						else:
							gate.execute('SELECT otp FROM marketPassTable WHERE username =?',(username,))
							data = gate.fetchall()
							st.warning("Already Applied, Cancel First, OTP = {}".format(data[0][0]))

			else:
				st.warning("Invalid Username/Password")							

def hideFooter():
    hide_streamlit_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {
	            visibility: hidden;
            }
            footer:after {
                content:'Made With ❤️ By MrTechnoStart'; 
                visibility: visible;
                display: block;
                position: relative;
                #background-color: red;
                padding: 5px;
                top: 2px;
            }
                        </style>
                        """
    st.markdown(hide_streamlit_style, unsafe_allow_html=True)
hideFooter()

main()
