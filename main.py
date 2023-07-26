import eel
from jinja2 import Template
from middle.adapter import *


def print_hi():
    options = {
        'mode': 'custom'
        # , 'args': ['/usr/local/bin/electron', '.'],
        #        (...)
    }

    eel.init('front')
    eel.start(
        'templates/base.html'
        , app_mode=False
        # , options=options
        # , suppress_error=True
        # , jinja_templates='templates'
    )
    # eel.start('main.html')#,
    # mode='default',
    # port=8080,
    # cmdline_args=['--start-fullscreen', '--browser-startup-dialog'])


if __name__ == '__main__':
    print_hi()
