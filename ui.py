import streamlit as st
from actions import actions, Action
from file_manager import FileManager
        

st.set_page_config(page_title='PDF Tools')

if 'action' not in st.session_state:
    st.title('PDF Tools')
else:
    st.title(st.session_state.action.title)

for action in actions:
    st.sidebar.button(action.title, on_click=action.callback)

if 'fmanager' not in st.session_state:
    st.session_state['fmanager'] = FileManager()

fmanager = FileManager.manager()
action = Action.action()

if action:
    fmanager.list_files()
    if not fmanager.is_empty:
        action.routine()
