# GatePass_Management_System
This is a Streamlit App which solves the problem of printing physical gatepass, thus, saving paper!


This repo has three .py files: 
1. users.py --> Uses Hashlib(Authentication & Encoding), sqlite3(For Database Management) : This is login page for students, to run:
```
streamlit run users.py
```
2. gateman.py --> Uses Hashlib(Authentication & Encoding), sqlite3(For Database Management) : This allow gateman to verify the OTP validity, to run:
```
streamlit run gateman.py
```
3. backend.py --> It's like the admin script, it allows admin to create more gateman and users, to run:
```
python backend.py
```

Note: 
run 
```
pip3 install -r requirements.txt
```
after cloning!!!
