import back.search
from back.search import *
import eel


@eel.expose
def search_adapter(text, section):
    print('search_adapter')
    print(text)
    print(section)
    return search(text, section)


@eel.expose
def add_doc_adapter(section):
    print('add_doc_adapter')
    add_doc(section)
    return 'Ok'


@eel.expose
def open_doc_adapter(target):
    print('open_doc_adapter')
    print(target)
    eel.show('templates/'+target)


@eel.expose
def get_doc_adapter(rowid):
    print('get_doc')
    print(rowid)
    return get_doc_by_id(rowid)


@eel.expose
def get_sections_adapter():
    print('get_sections')
    return get_sections()
