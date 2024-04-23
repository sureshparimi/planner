import streamlit as st
import sqlite3

def add_note(conn, note_name, note_content):
    c = conn.cursor()
    c.execute("INSERT INTO notes (note_name, note_content) VALUES (?, ?)", (note_name, note_content))
    conn.commit()

def get_notes(conn):
    c = conn.cursor()
    c.execute("SELECT * FROM notes")
    return c.fetchall()

def update_note_content(conn, note_id, modified_note_content):
    c = conn.cursor()
    c.execute("UPDATE notes SET note_content=? WHERE id=?", (modified_note_content, note_id))
    conn.commit()

def delete_note(conn, note_id):
    c = conn.cursor()
    c.execute("DELETE FROM notes WHERE id=?", (note_id,))
    conn.commit()

def show_notes_content(logged_in):
    st.write("### Notes")

    # Connect to SQLite3 database
    conn = sqlite3.connect('notes.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                note_name TEXT NOT NULL,
                note_content TEXT NOT NULL)''')

    if logged_in:
        note_name = st.text_input("Note Name")
        note_content = st.text_area("Note Content")
        if st.button("Add Note"):
            add_note(conn, note_name, note_content)

    notes = get_notes(conn)

    for note_id, note_name, note_content in notes:
        note_color = "#c4852f"  # You can generate unique colors dynamically if needed
        css_style = f"border: 2px solid {note_color}; border-radius: 10px; padding: 10px; margin-bottom: 10px;"
        st.markdown(f"<div style='{css_style}'>"
                    f"<h3>{note_name}</h3>"
                    f"<ol>{''.join(f'<li>{line}</li>' for line in note_content.split('\n'))}</ol>"
                    "</div>", unsafe_allow_html=True)

        edit_mode = st.session_state.get(f"edit_mode_{note_id}", False)  # Check edit mode for this note
        if edit_mode:
            modified_note_content = st.text_area("Modified Note Content", value=note_content)
            if st.button("Save"):
                update_note_content(conn, note_id, modified_note_content)
                st.session_state[f"edit_mode_{note_id}"] = False  # Exit edit mode after saving changes
                # Refresh the page or update UI to reflect changes
            elif st.button("Cancel"):
                st.session_state[f"edit_mode_{note_id}"] = False  # Exit edit mode without saving changes

        if st.button(f"Edit {note_name}"):
            st.session_state[f"edit_mode_{note_id}"] = True  # Set edit mode for this note

        if st.button(f"Delete {note_name}"):
            delete_note(conn, note_id)