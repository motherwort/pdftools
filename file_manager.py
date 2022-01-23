from tkinter import E
import streamlit as st
from datetime import datetime
import string
import random


class UploadedFile:
    def __init__(self, file):
        self.file = file
        self.checkbox = None
        
        self.id = None
    
    def connect_checkbox(self, checkbox):
        self.checkbox = checkbox

    @property
    def name(self):
        return self.file.name

    def get_random_key(self):
        random_id = ''.join(random.choice(string.ascii_lowercase) for i in range(5))
        self.id = random_id
        return random_id


class FileManager:
    def __init__(self):
        self.files = {}

    @staticmethod
    def manager():
        return st.session_state.get('fmanager', None)

    @property
    def is_empty(self):
        return len(self.files) == 0

    def list_files(self):
        self.container = st.container()
        with self.container:
            if not self.is_empty:
                for key, file in self.files.items():
                    cbox = st.checkbox(file.name, key=key)
                    file.connect_checkbox(cbox)
                st.button('Delete', help='Delete selected files', on_click=self.delete_selected)

        with st.form('my-form', clear_on_submit=True):
            files = st.file_uploader('Add PDF(s)', type='pdf', accept_multiple_files=True)
            submitted = st.form_submit_button('Add')
            
        if submitted and files is not None:
            self.files.update(self.get_file_dict(files))
            st.experimental_rerun()

    def get_file_dict(self, files):
        u_files = [UploadedFile(f) for f in files]
        return {file.get_random_key(): file for file in u_files}

    def delete_selected(self):
        to_save = []
        for file in self.files.values():
            if not file.checkbox:
                to_save.append(file)
        self.files = {}
        for file in to_save:
            self.files[file.get_random_key()] = file

    def get_file_list(self, preprocess=None):
        if preprocess is None:
            pp = lambda x: x
        else:
            pp = preprocess
        return list(map(pp, range(1, len(self.files) + 1)))

    def file_selector(self):
        # TODO сделать красивше (кодировать в виде "%номер в списке% %имя файла...%")
        return st.selectbox("Select file to process", options=self.get_file_list())

    def many_selector(self):
        # TODO кодировать в виде "%номер в списке% %имя файла...%"
        raise NotImplementedError

    def get_selected(self, selection):
        # TODO декодировать из номера в списке
        raise NotImplementedError
