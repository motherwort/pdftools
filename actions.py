from abc import ABCMeta, abstractmethod
import streamlit as st
import pdftools as pt
from file_manager import FileManager


MERGE = 'Merge PDFs'
SPLIT = 'Split two-page PDF'
CROP = 'Crop PDF'
EXTRACT = 'Extract pages from PDF'


class Action(metaclass=ABCMeta):
    @staticmethod
    def action():
        return st.session_state.get('action', None)

    @property
    @abstractmethod
    def title(self):
        pass

    @property
    def short_title(self):
        return self.title.split(' ')[0]

    def callback(self):
        st.session_state['action'] = self

    @abstractmethod
    def options(self):
        pass

    @abstractmethod
    def process(self, options):
        pass

    def routine(self):
        options = self.options()
        submit_button = st.button(self.short_title)
        if submit_button:
            # TODO сохранить результат в state, а выводить в другом месте (в result_manager???)
            result = self.process(options)
            st.button("Save")
            st.button("Further process")


# TODO добавить реальный функционал, доделать управление


class Merge(Action):
    title = MERGE

    def options(self):
        fmanager = FileManager.manager()
        order = st.text_input("Write down the order in which to merge files", 
            value=','.join(fmanager.get_file_list(str)))
        options = {
            'order': order
        }
        return options

    def process(self, options):
        st.write(list(map(int, options['order'].split(','))))


class Split(Action):
    title = SPLIT

    def options(self):
        fmanager = FileManager.manager()
        filenum = st.selectbox("Select file to process", 
                options=fmanager.get_file_list())

        options = {
            'filenum': filenum
        }
        return options

    def process(self, options):
        st.write(options['filenum'])


class Crop(Action):
    title = CROP

    def options(self):
        #TODO выбор страницы и её рендер
        #боксы для выбора границ
        pass

    def process(self, options):
        pass


class Extract(Action):
    title = EXTRACT

    def options(self):
        fmanager = FileManager.manager()
        filenum = fmanager.file_selector()
        order = st.text_input("Write down the numbers of pages or page intervals to extract from file", 
            placeholder='1,2,3,2,6,1-10,10-1,...')
        options = {
            'filenum': filenum,
            'order': order
        }
        return options

    def process(self, options):
        st.write(options['filenum'])
        st.write(options['order'].split(','))


actions = [
    Merge(),
    Split(),
    Crop(),
    Extract()
]
