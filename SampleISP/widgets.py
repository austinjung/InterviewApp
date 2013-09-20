__author__ = 'austin_45B_Kerkhoff'
from django.forms import ModelForm, DateTimeInput, CharField, TextInput
from django.conf import settings

class MyTextInputWidget(TextInput):
    class Media:
        css = {
            'all': (
                settings.STATIC_URL + 'css/ui/ui.base.css',
                settings.STATIC_URL + 'css/ui/ui.dialog.css',
            ),
        }
        js = (
            settings.STATIC_URL + 'js/jquery-1.9.0.js',
            settings.STATIC_URL + 'js/ui/ui.widget.js',
        )
