from django.db import models
from django.utils.translation import ugettext_lazy
from django.core.urlresolvers import reverse

import datetime
from django.utils import timezone

# Vendor Class : simple static class
# To show simple choice usage at Router class and switch class, I use a common python class instead of model class
# In real-world we usually keep this class in DB table using model class
class VENDOR(object):
    '''
    Simple Static Class for selected vendors information
    VENDOR_CHOICE : Selected Router/Switch Vendors
    PRIMARY_SUPPLIER : Primary supplier
    '''
    PRIMARY_SUPPLIER = 'CI'
    VENDOR_CHOICES = (
        ('CI', 'CISCO'),
        ('DL', 'D-Link'),
        ('AL', 'Alcatel-Lucent'),
    )

# Province Class : simple static class
# In real-world we usually keep this class in DB table using model class
class PROVINCE(object):
    '''
    Simple Static Class for selected vendors information
    VENDOR_CHOICE : Selected Router/Switch Vendors
    PRIMARY_SUPPLIER : Primary supplier
    '''
    DEFAULT_PROVINCE = 'BC'
    PROVINCE_CHOICES = (
        ('AB', 'Alberta'),
        ('BC', 'British Columbia'),
        ('NB', 'New Brunswick'),
        ('NL', 'Newfoundland and Labrador'),
        ('NS', 'Nova Scotia'),
        ('NT', 'Northwest Territories'),
        ('NU', 'Nunavut Territory'),
        ('ON', 'Ontario'),
        ('PE', 'Prince Edward Island'),
        ('QC', 'Quebec'),
        ('SK', 'Saskatchewan'),
        ('YT', 'Yukon Territory'),
    )


# Router Class
class Router(models.Model):
    '''
    Router class
    Router name for equipment maintenance will be auto-generated when Router Maker selected/changed
    ex) ISP-R-CI-00012345 : serial number will be auto-generated
    '''
    # explicitly define primary key with auto-increase integer field, 
    # to easy understand about auto-generation logic of router_name
    id = models.AutoField(primary_key=True)

    # assume this company buy routers from selected vendors
    router_model = models.CharField(max_length=50,
                                    db_column='model',
                                    verbose_name='Router Maker',
                                    help_text=ugettext_lazy('Router Maker'),
                                    choices=VENDOR.VENDOR_CHOICES,
                                    default=VENDOR.PRIMARY_SUPPLIER)

    # keep maintenance history to filter by last maintained date
    last_maintained_date = models.DateTimeField('Last Maintained Date')

    # Router name for equipment maintenance with model and serial NO.
    def router_name(self):
        return 'ISP-R-{0}-{1:08d}'.format(self.router_model, self.id)
    router_name.short_description = 'Router Name'

    def __unicode__(self):
        return self.router_name()

    def get_absolute_url(self):
        return reverse('SampleISP:router_detail', kwargs={'pk': self.pk})

# Switch Class
class Switch(models.Model):
    '''
    Switch class
    Switch name for equipment maintenance will be auto-generated when Switch Maker selected/changed
    ex) ISP-S-CI-00012345 : serial number will be auto-generated
    '''
    # explicitly define primary key with auto-increase integer field, 
    # to easy understand about auto-generation logic of switch_name
    id = models.AutoField(primary_key=True)

    # assume this company buy switches from selected vendors
    switch_model = models.CharField(max_length=50,
                                    db_column='model',
                                    verbose_name='Switch Maker',
                                    help_text=ugettext_lazy('Switch Maker'),
                                    choices=VENDOR.VENDOR_CHOICES,
                                    default=VENDOR.PRIMARY_SUPPLIER)

    # keep maintenance history to filter by last maintained date
    last_maintained_date = models.DateTimeField('Last Maintained Date')

    # Switch name for equipment maintenance with model and serial NO.
    def switch_name(self):
        return 'ISP-S-{0}-{1:08d}'.format(self.switch_model, self.id)
    switch_name.short_description = 'Switch Name'

    def __unicode__(self):
        return self.switch_name()

    class Meta:
        verbose_name_plural = ugettext_lazy("Switches")


# Remote Access Server Class
class RAS(models.Model):
    '''
    Remote Access Server class
    RAS name for equipment maintenance will be auto-generated when RAS Maker selected/changed
    ex) ISP-R-CI-00012345 : serial number will be auto-generated
    '''
    # explicitly define primary key with auto-increase integer field, 
    # to easy understand about auto-generation logic of ras_name
    id = models.AutoField(primary_key=True)

    # assume this company buy Remote Access Servers from selected vendors
    ras_model = models.CharField(max_length=50,
                                 db_column='model',
                                 verbose_name='Remote Access Server Maker',
                                 help_text=ugettext_lazy('Remote Access Server Maker'),
                                 choices=VENDOR.VENDOR_CHOICES,
                                 default=VENDOR.PRIMARY_SUPPLIER)

    # keep maintenance history to filter by last maintained date
    last_maintained_date = models.DateTimeField('Last Maintained Date')

    # RAS name for equipment maintenance with model and serial NO.
    def ras_name(self):
        return 'ISP-R-{0}-{1:08d}'.format(self.ras_model, self.id)
    ras_name.short_description = 'Remote Access Server Name'

    def __unicode__(self):
        return self.ras_name()

    class Meta:
        verbose_name = ugettext_lazy("Remote Access Server")


# Customer Class
class Customer(models.Model):
    customerID = models.CharField(max_length=100, 
                                  help_text=ugettext_lazy('Customer ID'),
                                  default="New Customer ID",
                                  unique=True)
    first_name = models.CharField(max_length=50, help_text=ugettext_lazy('First name'))
    last_name = models.CharField(max_length=50, help_text=ugettext_lazy('Last name'))
    email = models.EmailField(max_length=75, help_text=ugettext_lazy('Email'))
    street = models.CharField(max_length=50, help_text=ugettext_lazy('Street'))
    city = models.CharField(max_length=50, help_text=ugettext_lazy('City'))
    province = models.CharField(max_length=50, 
                                help_text=ugettext_lazy('Province'),
                                choices=PROVINCE.PROVINCE_CHOICES,
                                default=PROVINCE.DEFAULT_PROVINCE)
    subscribed_date = models.DateTimeField('Date subscribed')

    def full_name(self):
        return "%s %s" % (self.first_name, self.last_name)
    full_name.short_description = 'Full name'

    def save(self, *args, **kwargs):
        super(Customer, self).save(*args, **kwargs)
        self.customerID = 'ISP-CUST-{0:08d}'.format(self.id)
        return super(Customer, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.full_name()


# Router Port Class
class RouterPort(models.Model):
    '''
    RouterPort Class : Ports of routers
    a router port can be connected with a switch
    '''
    port_name = models.CharField(max_length=20,
                                 verbose_name='Port name on router',
                                 help_text=ugettext_lazy('Port name on this router'))
    router = models.ForeignKey(Router)
    #switch field should be accept NULL to present a port is not connected with a switch
    switch = models.ForeignKey(Switch,null=True,blank=True,
                               verbose_name='Connected Switch',
                               help_text=ugettext_lazy('Switch which is connected to this router port'))

    # router port name with router name and port name.
    def router_port_name(self):
        return "%s : %s" % (self.router.router_name(), self.port_name)
    router_port_name.short_description = 'Router Port Name'

    def __unicode__(self):
        return self.router_port_name()

    def get_absolute_url(self):
        # return reverse('SampleISP:routerport_detail', kwargs={'pk': self.pk})
        return reverse('SampleISP:routerport_list')

    def save(self, *args, **kwargs):
        return super(RouterPort, self).save(*args, **kwargs)


# Switch Port Class
class SwitchPort(models.Model):
    '''
    SwitchPort Class : Ports of switches
    a switch port can be connected with a Remote Access Server
    '''
    port_name = models.CharField(max_length=20,
                                 verbose_name='Port name on switch',
                                 help_text=ugettext_lazy('Port name on this switch'))
    switch = models.ForeignKey(Switch)
    #ras field should be accept NULL to present a port is not connected with a Remote Access Server
    ras = models.ForeignKey(RAS,null=True,blank=True,
                            verbose_name='Connected Remote Access Server',
                            help_text=ugettext_lazy('Remote Access Server which is connected to this switch port'))

    # switch port name with switch name and port name.
    def switch_port_name(self):
        return "%s : %s" % (self.switch.switch_name(), self.port_name)
    switch_port_name.short_description = 'Switch Port Name'

    def __unicode__(self):
        return self.switch_port_name()


# IPaddress Class
class IPaddress(models.Model):
    '''
    IPaddress Class : IP addresses which Remote Access Servers can issue
    a IP address can be assigned to a customer
    '''
    ip_address = models.GenericIPAddressField(max_length=50, 
                                              verbose_name='IP address',
                                              help_text=ugettext_lazy('IP address which is issued to a customer by a Remote Access Server.'))
    # IP addresse which a RAS can be assigned from their switches
    ras = models.ForeignKey(RAS,
                            verbose_name='Remote Access Server',
                            help_text=ugettext_lazy('Remote Access Server which issue an IP address to a customer.'))
    # customer field should be accept NULL to present a IP address is not assigned to a customer
    customer = models.ForeignKey(Customer,null=True,blank=True,
                                 verbose_name='Assigned Customer',
                                 help_text=ugettext_lazy('Customer to whom an IP address is issued by a Remote Access Server.'))

    # IP address name with switch name and IP address.
    def ip_address_name(self):
        return "%s : %s" % (self.ras.ras_name(), self.ip_address)
    ip_address_name.short_description = 'IP Address Name'

    def __unicode__(self):
        return self.ip_address_name()

    class Meta:
        verbose_name = ugettext_lazy("IP Address")
        verbose_name_plural = ugettext_lazy("IP Addresses")
