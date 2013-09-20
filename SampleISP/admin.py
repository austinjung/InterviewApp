from SampleISP.models import Router, Switch, RAS, Customer, RouterPort, SwitchPort, IPaddress
from django.contrib import admin

'''
Router section
'''
class RouterPortTabularInline(admin.TabularInline):
    model = RouterPort
    extra = 1

class RouterAdmin(admin.ModelAdmin):
    readonly_fields = ('router_name',)
    fieldsets = [
        ('Router',              {'fields': ['router_name','router_model']}),
        ('Last Maintained Date',{'fields': ['last_maintained_date'], 'classes': ['collapse']}),
    ]
    inlines = [RouterPortTabularInline]
    list_display = ('router_name', 'router_model','last_maintained_date',)
    list_filter = ['last_maintained_date']
    search_fields = ['router_model','id']

admin.site.register(Router, RouterAdmin)

'''
Switch Section
'''
class SwitchPortTabularInline(admin.TabularInline):
    model = SwitchPort
    extra = 1

class SwitchAdmin(admin.ModelAdmin):
    readonly_fields = ('switch_name',)
    fieldsets = [
        ('Switch',              {'fields': ['switch_name','switch_model']}),
        ('Last Maintained Date',{'fields': ['last_maintained_date'], 'classes': ['collapse']}),
    ]
    inlines = [SwitchPortTabularInline]
    list_display = ('switch_name', 'switch_model','last_maintained_date',)
    list_filter = ['last_maintained_date']
    search_fields = ['switch_model','id']

admin.site.register(Switch, SwitchAdmin)

'''
Remote Access Server Section
'''
class IPaddressTabularInline(admin.TabularInline):
    model = IPaddress
    extra = 1

class RASAdmin(admin.ModelAdmin):
    readonly_fields = ('ras_name',)
    fieldsets = [
        ('Remote Access Server',{'fields': ['ras_name','ras_model']}),
        ('Last Maintained Date',{'fields': ['last_maintained_date'], 'classes': ['collapse']}),
    ]
    inlines = [IPaddressTabularInline]
    list_display = ('ras_name', 'ras_model','last_maintained_date',)
    list_filter = ['last_maintained_date']
    search_fields = ['ras_model','id']

admin.site.register(RAS, RASAdmin)

'''
Customer Section
'''
class CustomerAdmin(admin.ModelAdmin):
    readonly_fields = ('customerID',)
    fieldsets = [
        ('Customer Information',    {'fields': [('customerID','first_name','last_name','email'),
                                                ('street','city','province')]}),
        ('Subscribed Date',         {'fields': ['subscribed_date'], 'classes': ['collapse']}),
    ]
    inlines = [IPaddressTabularInline]
    list_display = ('customerID','first_name','last_name','email',
                    'street','city','province','subscribed_date')
    list_filter = ['province','subscribed_date']
    search_fields = ['customerID','first_name','last_name','email',
                     'street','city','province']

admin.site.register(Customer, CustomerAdmin)
