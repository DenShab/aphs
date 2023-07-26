import eel
from jinja2 import Template
from middle.adapter import *


def print_hi():
    eel.init('front')
    eel.start(
        'templates/base.html'#,
       # jinja_templates='templates'
    )
    # eel.start('main.html')#,
    # mode='defult',
    # port=8080,
    # cmdline_args=['--start-fullscreen', '--browser-startup-dialog'])


if __name__ == '__main__':
    print_hi()
