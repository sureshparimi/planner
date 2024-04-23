import streamlit as st
import sqlite3
from datetime import datetime

def add_meeting(conn, meeting_name, meeting_date, meeting_time, action_items):
    c = conn.cursor()
    # Convert meeting_time to string before inserting into the database
    meeting_time_str = meeting_time.strftime('%H:%M:%S')
    c.execute("INSERT INTO meetings (meeting_name, meeting_date, meeting_time, action_items) VALUES (?, ?, ?, ?)",
              (meeting_name, meeting_date, meeting_time_str, action_items))
    conn.commit()

def get_meetings(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM meetings")
    return c.fetchall()

def delete_meeting(conn, meeting_id):
    c = conn.cursor()
    c.execute("DELETE FROM meetings WHERE id=?", (meeting_id,))
    conn.commit()

def show_meetings_content(logged_in):
    st.write("### Meetings")

    # Connect to SQLite3 database
    conn = sqlite3.connect('meetings.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS meetings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                meeting_name TEXT NOT NULL,
                meeting_date DATE NOT NULL,
                meeting_time TEXT NOT NULL,
                action_items TEXT NOT NULL)''')

    if logged_in:
        meeting_name = st.text_input("Meeting Name")
        meeting_date = st.date_input("Meeting Date")
        meeting_time = st.time_input("Meeting Time")
        action_items = st.text_area("Action Items")
        if st.button("Add Meeting"):
            add_meeting(conn, meeting_name, meeting_date, meeting_time, action_items)

    meetings = get_meetings(conn)

    for meeting in meetings:
        meeting_id, meeting_name, meeting_date, meeting_time, action_items = meeting
        meeting_color = "#c4852f"  # You can generate unique colors dynamically if needed
        css_style = f"border: 2px solid {meeting_color}; border-radius: 10px; padding: 10px; margin-bottom: 10px;"
        st.markdown(f"<div style='{css_style}'>"
                    f"<h3>{meeting_name}</h3>"
                    f"<p>Date: {meeting_date}</p>"
                    f"<p>Time: {meeting_time}</p>"
                    f"<p>Action Items:</p>"
                    f"<ul>{''.join([f'<li>{line}</li>' for line in action_items.split('\n')])}</ul>"
                    f"<button onclick='deleteMeeting({meeting_id})'>Delete</button>"
                    "</div>", unsafe_allow_html=True)

    # JavaScript function to handle meeting deletion
    st.markdown(
        """
        <script>
            function deleteMeeting(meetingId) {
                var confirmed = confirm("Are you sure you want to delete this meeting?");
                if (confirmed) {
                    window.location.href = `?delete_meeting=${meetingId}`;
                }
            }
        </script>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    logged_in = True  # Assume user is logged in for demonstration purposes
    show_meetings_content(logged_in)
