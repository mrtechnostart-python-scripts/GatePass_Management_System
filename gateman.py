import sqlite3
import streamlit as st
import pandas as pd
import hashlib


conn = sqlite3.connect('watchman.db')
c = conn.cursor()


gatePass = sqlite3.connect('gatepass.db')
gate = gatePass.cursor()

gate.execute('CREATE TABLE IF NOT EXISTS marketPassTable(username TEXT,otp TEXT,datetime TEXT,expectedDateTime TEXT)')
def check_otp(username,userOTP):
    gate.execute('SELECT otp FROM marketPassTable WHERE username =?',(username,))
    data = gate.fetchall()
    if str(userOTP) == data[0][0]:
        return True
    return False


def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()

def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False


def login_user(username,password):
	c.execute('SELECT * FROM watchManTable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data


def deleteData(username,userOTP):
    gate.execute("SELECT username,otp from marketPassTable where username =? and otp=?",(username,userOTP))
    data = gate.fetchall()
    if data:
        gate.execute('DELETE FROM marketPassTable WHERE username =? AND otp=?',(username,userOTP,))
        gatePass.commit()
        st.success("Deleted SuccessFully!")
    else:
        st.warning("Record Not Found!")



def main():
	"""Simple Login App"""

	st.title("Simple Login App")

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
				task = st.selectbox("Tasks",["Check Gate Pass", "Remove Gate Pass"])
				if task == "Check Gate Pass":
					userName = st.text_input("Enter User Name")
					userOTP =  st.text_input("Enter OTP Here: ")

					if st.button("Submit: "):
						if check_otp(userName,userOTP):
							st.success("You Can Go! OTP is Correct! Good Journeys {}".format(userName))
						else:
							st.warning("Invalid OTP!")
							
				elif task == "Remove Gate Pass":
					userName = st.text_input("Enter User Name")
					userOTP =  st.text_input("Enter OTP Here: ")

					if st.button("Submit: "):
						deleteData(userName,userOTP)
					

main()
