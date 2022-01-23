import streamlit as st
import pdftools as pt
from datetime import datetime
import string
import random


class Action:
    def __init__(self, title, short_title=None):
        self.title = title
        if short_title:
            self.short_title = short_title
        else:
            self.short_title = title.split(' ')[0]

    # def view(self):
    #     st.session_state['action'] = self


actions = [
    Action('Merge PDFs'),
    Action('Split two-page PDF'),
    Action('Crop PDF'),
    Action('Extract pages from PDF')
]


class UploadedFile:
    def __init__(self, file):
        self.file = file
        self.checkbox = None
        
        self.id = None
    
    def add_checkbox(self, checkbox):
        self.checkbox = checkbox

    @property
    def name(self):
        return self.file.name

    def get_random(self):
        random_id = ''.join(random.choice(string.ascii_lowercase) for i in range(5))
        self.id = random_id
        return random_id
        

# def home_view():
#     if 'title' in st.session_state:
#         st.session_state.pop('title')


def merge_view():
    st.session_state['action'] = actions[0]
    pass


def split_view():
    st.session_state['action'] = actions[1]
    pass


def crop_view():
    st.session_state['action'] = actions[2]
    pass


def extract_view():
    st.session_state['action'] = actions[3]
    pass


st.set_page_config(page_title='PDF Tools')

if 'action' not in st.session_state:
    st.title('PDF Tools')
else:
    st.title(st.session_state.action.title)

# st.sidebar.button('Home', on_click=home_view)
st.sidebar.button(actions[0].title, on_click=merge_view)
st.sidebar.button(actions[1].title, on_click=split_view)
st.sidebar.button(actions[2].title, on_click=crop_view)
st.sidebar.button(actions[3].title, on_click=extract_view)


def delete_view():
    if 'files' in st.session_state:
        to_save = []
        for key, file in st.session_state.files.items():
            if not file.checkbox:
                to_save.append(file)
        if len(to_save) == 0:
            st.session_state.pop('files')
        else:
            st.session_state.pop('files')
            st.session_state['files'] = {}
            for file in to_save:
                st.session_state.files[file.get_random()] = file 



if 'action' in st.session_state:
    file_container = st.container()
    with file_container:
        if 'files' in st.session_state:
            for key, file in st.session_state.files.items():
                cbox = st.checkbox(file.name, key=key)
                file.add_checkbox(cbox)
            delete_button = st.button("Delete", on_click=delete_view)

    with st.form("my-form", clear_on_submit=True):
        files = st.file_uploader('Add PDF(s)', type='pdf', accept_multiple_files=True)
        submitted = st.form_submit_button("Add PDF(s)")
    if submitted and files is not None:
        if 'files' in st.session_state:
            u_files = [UploadedFile(f) for f in files]
            st.session_state.files.update({file.get_random(): file for file in u_files})
        else:
            u_files = [UploadedFile(f) for f in files]
            st.session_state['files'] = {file.get_random(): file for file in u_files}
        st.experimental_rerun()

    if 'files' in st.session_state:
        
        order = st.text_input("Write down order of uploaded files", 
            value=','.join(list(map(str, range(1, len(st.session_state.files) + 1)))))

        submit_button = st.button(st.session_state.action.short_title)

        if submit_button:
            st.write(list(map(int, order.split(','))))
            pass


    

    

    

