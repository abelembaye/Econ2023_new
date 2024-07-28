
# streamlit run sqlite_learn2_eachUser.py
import streamlit as st
import sqlite3
import pandas as pd
import os
import sys

wdir = r'C:\Users\aembaye\Documents\dbcontainer'
filename = "aembaye_database2.db"

full_path = os.path.join(wdir, filename)

# sys.exit()

conn = sqlite3.connect(full_path, check_same_thread=False)

cursor = conn.cursor()


def formCreation():
    st.write('Please fill in this form')
    with st.form(key="Form1"):
        username = st.text_input('Enter your username: ')
        q1 = st.text_input('Enter your name: ')
        q2 = st.number_input("Enter your age: ")
        q3 = st.text_input('Enter your country: ')
        q4 = st.text_input('Enter your country of birth: ')
        q5 = st.date_input('Enter the date: ')
        # q6 = st.file_uploader('Enter image: ')
        submit = st.form_submit_button(label='submit')

    if submit == True:
        st.success('Your registration has been successfull')
        addInfo(username, q1, q2, q3, q4, q5)


def addInfo(a, b, c, x, y, z):
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS table2 (USERNAME TEXT (50) PRIMARY KEY, q1 TEXT(50), q2 FLOAT, q3 TEXT(50), q4 TEXT, q5 TEXT(50))
        """
    )

    cursor.execute("SELECT * FROM table2 WHERE USERNAME = ?", (a,))
    row = cursor.fetchone()

    if row is None:
        cursor.execute(
            "INSERT INTO table2 VALUES (?,?,?,?,?, ?)", (a, b, c, x, y, z))
    else:
        cursor.execute(
            "UPDATE table2 SET q1 = ?, q2 = ?, q3 = ?, q4 = ?, q5 = ? WHERE USERNAME = ?", (b, c, x, y, z, a))

    conn.commit()
    st.success('User has been added to the SQLITE database')


formCreation()

# New code to display the table as a DataFrame
try:
    df = pd.read_sql_query("SELECT * FROM table2", conn)
    st.write(df)
except pd.io.sql.DatabaseError:
    st.error('The table does not exist yet.')
