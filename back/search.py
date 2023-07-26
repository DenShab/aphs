from tkinter import Tk
from tkinter.filedialog import askopenfilename
import win32com.client as win32
from bs4 import BeautifulSoup
import base64

from back import database
import os, shutil
import sys
import mammoth
import regex as re
import configparser

if getattr(sys, 'frozen', False):
    application_path = os.path.dirname(sys.executable)
elif __file__:
    application_path = os.path.dirname(__file__)

config_path = os.path.join(application_path, 'config')
print(config_path)
config = configparser.ConfigParser()
config.read(config_path)
path1 = config.get('config', 'pathbd')
bd_path = os.path.join(application_path, path1)
print(bd_path)
db = database.Database(os.path.join(os.path.dirname(sys.executable), bd_path))


def add_doc(section):
    print('add_doc')

    filetypes = (("Word", "*.docx *.jpg"),
                 ("Любой", "*"))
    root = Tk()
    root.attributes('-topmost', True)  # Display the dialog in the foreground.
    root.iconify()  # Hide the little window.
    filename = askopenfilename(title='Выберете документ/документы', parent=root, multiple=True, filetypes=filetypes)
    root.destroy()  # Destroy the root window when folder selected.
    if filename:
        print(filename)
        if isinstance(filename, str):
            add(filename, section)
        else:
            for doc_name in filename:
                add(doc_name, section)
    print('end add_doc')

    # map(lambda doc_name: add(doc_name), filename)


def add(doc_name, section):
    data = list()
    data.append(doc_name.split('/')[-1])
    # Load the document from disk

    # Open MS Word
    word = win32.gencache.EnsureDispatch('Word.Application')
    doc_path = doc_name.replace('/', '\\')
    doc = word.Documents.Open(doc_path)
    # change to a .html
    # txt_path = wordFilePath.split('.')[0] + '.html'

    # wdFormatFilteredHTML has value 10
    # saves the doc as an html
    html_name = doc_name.split('/')[-1].split('.')[0] + '.html'
    path_list = doc_name.split('/')
    path_list[-1] = html_name
    html_path = '\\'.join(path_list)
    html_path_src = html_path.replace('.html', '.files')

    doc.SaveAs(html_path, 10)

    doc.Close()

    # noinspection PyBroadException
    try:
        word.ActiveDocument()
    except Exception:
        word.Quit()
    html_file = open(html_path, 'r', encoding='windows-1251')
    html_code = html_file.read()
    soup = BeautifulSoup(html_code, "html.parser")
    # the_contents_of_body_without_body_tags = []
    # for data in body.findChildren(recursive=False):
    #  the_contents_of_body_without_body_tags.append(data.text)

    for link in soup.findAll('img'):
        # <img width="182" height="544" src="Ins_003.files/image001.jpg">
        with open(html_path_src + '/' + link.get('src').split('/')[1], 'rb') as html_file:
            data_uri = base64.b64encode(html_file.read()).decode('utf-8')
        img_tag = soup.new_tag('img')
        img_tag['src'] = 'data:image/gif;base64,{0}'.format(data_uri)
        # img_tag = '<img src="data:image/png;base64,{0}">'.format(data_uri)
        if link.has_attr('alt'):
            img_tag['alt'] = link['alt']
        link.replace_with(img_tag)

    os.remove(html_path.replace('\\', '/'))
    folder = html_path_src.replace('\\', '/')
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))
    os.rmdir(html_path_src.replace('\\', '/'))

    with open(doc_name, "rb") as docx_file:
        result_text = mammoth.extract_raw_text(docx_file)

    body = soup.find('body')
    the_contents_of_body_without_body_tags = str(body.findChildren(recursive=False))

    text = result_text.value
    text = " ".join(re.sub(r'[^\pL\p{Space}]', '', text).strip().split())

    data.append(section)
    data.append(text)
    data.append(the_contents_of_body_without_body_tags)
    data.append('')
    db.add_new_doc(data)
    # db.add_section(section)


def search(text, section):
    text = " ".join(re.sub(r'[^\pL\p{Space}]', '', text).strip().split())
    print(text)

    if text != '':
        docs = search_doc_by_text(text, section)
    else:
        docs = search_doc_without_text(section)

    res = list()
    for doc in docs:
        values = list()
        for d in doc:
            if isinstance(d, int):
                info = d
            else:
                info = (d[:650] + '...') if len(d) > 650 else d
            values.append(info)
        res.append(values)
    print(res)
    return res


def search_doc_by_text(text, section):
    return db.search_doc_by_text(text, section)


def search_doc_without_text(section):
    return db.search_doc_without_text(section)


def get_doc_by_id(rowid):
    return db.search_doc_by_id(rowid)


def get_sections():
    return db.get_sections()
