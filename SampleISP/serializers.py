__author__ = 'austin_45B_Kerkhoff'
from rest_framework import serializers
from SampleISP.models import VENDOR, PROVINCE, Router, Switch, IPaddress, \
                             RAS, Customer, RouterPort, SwitchPort

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model = VENDOR

class ProvinceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PROVINCE

class RouterSerializer(serializers.ModelSerializer):
    router_name = serializers.SerializerMethodField('get_name')
    class Meta:
        model = Router
        fields = ('id','router_name','router_model', 'last_maintained_date')
    def get_name(self, obj):
        return 'ISP-R-{0}-{1:08d}'.format(obj.router_model, obj.id)

class SwitchSerializer(serializers.ModelSerializer):
    switch_name = serializers.SerializerMethodField('get_name')
    class Meta:
        model = Switch
        fields = ('id','switch_name','switch_model', 'last_maintained_date')
    def get_name(self, obj):
        return 'ISP-S-{0}-{1:08d}'.format(obj.switch_model, obj.id)

class RouterPortSerializer(serializers.ModelSerializer):
    router = RouterSerializer(required=True)
    switch = SwitchSerializer(required=True)
    class Meta:
        model = RouterPort
        fields = ('id', 'port_name', 'router', 'switch',)
