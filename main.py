import streamlit as st
import sqlite3
from notes import show_notes_content
from meetings import show_meetings_content

# Function to create users table if not exists
def create_users_table(conn):
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL)''')
    conn.commit()

# Function to add user to users table
def add_user(conn, username, password):
    c = conn.cursor()
    c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
              (username, password))
    conn.commit()

# Function to check if user exists in users table
def user_exists(conn, username):
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=?", (username,))
    return c.fetchone() is not None

# Function to authenticate user
def authenticate_user(conn, username, password):
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?",
              (username, password))
    return c.fetchone()

# Function to handle login
def login(conn):
    st.write("### Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if username and password:
            user = authenticate_user(conn, username, password)
            if user:
                # Set logged_in flag to True
                st.session_state.logged_in = True
                return True  # Return True after successful login
            else:
                st.error("Invalid username or password.")
        else:
            st.warning("Please enter username and password.")
    return False  # Return False if login fails

# Function to handle registration
def register(conn):
    st.write("### Register")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        if username and password:
            if not user_exists(conn, username):
                add_user(conn, username, password)
                st.success("Registration successful! Please login.")
            else:
                st.warning("Username already exists. Please choose a different one.")
        else:
            st.warning("Please enter username and password.")

# Connect to SQLite3 database
conn = sqlite3.connect('users.db')
create_users_table(conn)

# Check if user is logged in
if not st.session_state.get('logged_in', False):
    # Show login by default
    if login(conn):
        # Redirect to selected page after successful login
        selected_page = st.session_state.get('selected_page', 'Notes')
        st.experimental_set_query_params(logged_in=True, page=selected_page)
        st.stop()

# Show navigation links
st.write("[Daily Plan](?page=Daily%20Plan) | [Meetings](?page=Meetings) | [Notes](?page=Notes)")

# Show dropdown menu for page selection
selected_page = st.sidebar.selectbox("Select Page", ["Daily Plan", "Meetings", "Notes"])

# Store selected page in session state
st.session_state.selected_page = selected_page

# Show content based on selected page
if selected_page == "Daily Plan":
    st.write("Daily Plan content goes here.")
elif selected_page == "Meetings":
    show_meetings_content(st.session_state.get('logged_in', False))  # Call the function from meetings.py to display meetings content
elif selected_page == "Notes":
    show_notes_content(st.session_state.get('logged_in', False))  # Pass logged_in status to show_notes_content
