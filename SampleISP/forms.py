__author__ = 'austin_45B_Kerkhoff'
from django.forms.util import ErrorList
from django.forms import ModelForm, DateTimeInput, CharField, TextInput, model_to_dict
from SampleISP.models import VENDOR, PROVINCE, Router, Switch, IPaddress, \
                             RAS, Customer, RouterPort, SwitchPort
from django.forms.models import BaseModelFormSet, modelformset_factory, inlineformset_factory
from django.conf import settings
from SampleISP.widgets import MyTextInputWidget

class RouterForm(ModelForm):
    router_name = CharField(
        widget=TextInput(attrs={'class': 'sortable', 'readonly':'readonly'}),
        initial='Initial Value',
    )
    class Meta:
        model = Router
        fields = ('router_name','router_model','last_maintained_date',)
        # exclude = ('id',)
        widgets = {
            'last_maintained_date': DateTimeInput(attrs={'class':'sortable',}),
            # 'router_name': TextInput(attrs={'class': 'sortable', 'value':'Router_Name', 'readonly':'readonly'}),
        }

class FormSetWithExtra(BaseModelFormSet):
    def add_fields(self, form, index):
        super(FormSetWithExtra,self).add_fields(form, index)
        form.fields['extra_field'] = CharField(required=False)

RouterPortFormSet = modelformset_factory(RouterPort,
                                         extra=1,
                                         can_order=False, can_delete=False)

RouterPortFormSetWithExtra = modelformset_factory(RouterPort,
                                                  formset=FormSetWithExtra,
                                                  extra=1,
                                                  can_order=False, can_delete=False)

class SwitchForm(ModelForm):
    class Meta:
        model = Switch

class RouterPortForm(ModelForm):
    class Meta:
        model = RouterPort
        # widgets = {
        #     'port_name': MyTextInputWidget(
        #         attrs={'class': 'sortable', 'readonly':'readonly'}
        #     ),
        # }
    class Media:
        css = {
            'all': (
                settings.STATIC_URL + 'css/themes/camtran/jquery-ui-1.8.6.custom.css',
            ),
        }
        js = (
            settings.STATIC_URL + 'js/jquery-1.9.0.js',
            settings.STATIC_URL + 'js/jquery-ui-1.10.0.custom.js',
        )

    def is_valid(self):
        if self:
            if self.initial['port_name'] != self.data['port_name']:
                port_name_changed = True
            else:
                port_name_changed = False
            if str(self.initial['router']) != self.data['router']:
                router_changed = True
            else:
                router_changed = False
            if str(self.initial['switch']) != self.data['switch']:
                switch_changed = True
            else:
                switch_changed = False
            is_valid = super(RouterPortForm, self).is_valid()
            return is_valid
        else:
            return False

class SwitchPortForm(ModelForm):
    class Meta:
        model = SwitchPort

class CustomerForm(ModelForm):
    class Meta:
        model = Customer

class RASForm(ModelForm):
    ras_name = CharField(
        widget=TextInput(attrs={'class': 'sortable', 'readonly':'readonly'}),
        initial='Initial Value',
    )
    class Meta:
        model = RAS
        fields = ('ras_name','ras_model','last_maintained_date',)

class IPaddressForm(ModelForm):
    class Meta:
        model = IPaddress

IPaddressInlineFormSet = inlineformset_factory(RAS, IPaddress, extra=1)