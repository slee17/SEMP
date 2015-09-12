from django.conf import settings
import os

# django-fullcalendar static file location defaults to FullCalendar default 
# folder structure, expected to be under the STATIC_URL

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # Get the location of this file
                                                                       # and go up two directories.
"""
FULLCALENDAR_DEFAULTS = {
    'css_url': '//cdnjs.cloudflare.com/ajax/libs/fullcalendar/1.6.4/fullcalendar.css',
    'print_css_url': '//cdnjs.cloudflare.com/ajax/libs/fullcalendar/1.6.4/fullcalendar.print.css',
    'javascript_url': '//cdnjs.cloudflare.com/ajax/libs/fullcalendar/1.6.4/fullcalendar.min.js',
    # 'javascript_url': os.path.join(BASE_DIR, 'static/fullcalendar/fullcalendar.min.js'),
    'jquery_url': '//code.jquery.com/jquery-2.1.0.min.js',
    'jquery_ui_url': '//code.jquery.com/ui/1.10.4/jquery-ui.js',
}

FULLCALENDAR_DEFAULTS = {
    'css_url': '//cdnjs.cloudflare.com/ajax/libs/fullcalendar/2.3.2/fullcalendar.css',
    'print_css_url': '//cdnjs.cloudflare.com/ajax/libs/fullcalendar/2.3.2/fullcalendar.print.css',
    'javascript_url': '//cdnjs.cloudflare.com/ajax/libs/fullcalendar/2.3.2/fullcalendar.min.js',
    # 'javascript_url': os.path.join(BASE_DIR, 'static/fullcalendar/fullcalendar.min.js'),
    'jquery_url': '//code.jquery.com/jquery-2.1.0.min.js',
    'jquery_ui_url': '//code.jquery.com/ui/1.10.4/jquery-ui.js',
}
"""

FULLCALENDAR_DEFAULTS = {
    'css_url': '//cdnjs.cloudflare.com/ajax/libs/fullcalendar/2.3.2/fullcalendar.css'
    'print_css_url': '//cdnjs.cloudflare.com/ajax/libs/fullcalendar/2.3.2/fullcalendar.print.css'
    'moment_url': '//cdnjs.cloudflare.com/ajax/libs/moment.js/2.9.0/moment.min.js'
    <script type='text/javascript' src=></script>
    <script src='//code.jquery.com/jquery-2.1.3.min.js'></script>
    <script src='//code.jquery.com/ui/1.10.4/jquery-ui.js'></script>
    <script src='//cdnjs.cloudflare.com/ajax/libs/fullcalendar/2.3.2/fullcalendar.min.js'></script>
}
    # 'jquery_url': '//code.jquery.com/jquery-1.11.3.min.js',
    # 'jquery_ui_url': '//code.jquery.com/ui/1.11.4/jquery-ui.js',

# Updates location based on configuration defined by 
# settings.py of the project

FULLCALENDAR = FULLCALENDAR_DEFAULTS.copy()
FULLCALENDAR.update(getattr(settings, 'FULLCALENDAR', {}))

def css_url():
    return FULLCALENDAR['css_url']

def print_css_url():
    return FULLCALENDAR['print_css_url']

def javascript_url():
    return FULLCALENDAR['javascript_url']

def jquery_url():
    return FULLCALENDAR['jquery_url']

def jquery_ui_url():
    return FULLCALENDAR['jquery_ui_url']