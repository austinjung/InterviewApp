"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.utils import unittest
from django.test.client import Client
from django.contrib.auth.models import User
import datetime
from django.utils.timezone import utc
from SampleISP.models import Router, Switch, RouterPort
from SampleISP.forms import RouterForm

from django.test import LiveServerTestCase
from splinter import Browser
from time import sleep

class RouterTestCase(TestCase):
    def setUp(self):
        """
        Every test needs create each one instance for Router
        """
        self.router = Router.objects.create(router_model="AL", last_maintained_date=datetime.datetime(2013, 07, 16, 13, 9, 25, tzinfo=utc))

    def test_router_name(self):
        """
        Router's router_name field is not a part of table column.
        This should be generated from other fields of Router
        """
        self.assertEqual(self.router.router_name(), 'ISP-R-{0}-{1:08d}'.format(self.router.router_model, self.router.id))


class HttpClientTestCase(unittest.TestCase):
    def setUp(self):
        """
        Every test needs a client and test_account.
        """
        self.client = Client(enforce_csrf_checks=True)
        try:
            self.user = User.objects.get(username="test_account")
        except Exception as e:
            self.user = User.objects.create_user("test_account", "", "password")

    def test_login(self):
        """
        Test login with test account.
        """
        #using standard Django authorization login
        login_result = self.client.login(username='test_account', password='password')
        self.assertEqual(login_result, True)

    def test_login_post(self):
        """
        Test login with posting test account.
        """
        self.client = Client(enforce_csrf_checks=False)
        #using post to login page
        response = self.client.post('/admin/', {'username': 'test_account', 'password': 'password'})
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

    def test_list_tables(self):
        """
        Test default page of this app which list tables
        """
        # Issue a GET request.
        login_result = self.client.login(username='test_account', password='password')
        self.assertEqual(login_result, True)
        response = self.client.get('/SampleISP/')

        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check that the rendered context contains Table List.
        self.assertEqual(len(response.context), 2)
        table_list = ({'url':'customers','table_name':'Customers'},
                      {'url':'routers','table_name':'Routers'},
                      {'url':'routerports','table_name':'RouterPorts'},
                      {'url':'routerports/manage','table_name':'Manage RouterPorts'},
                      {'url':'routerports/new_manage','table_name':'Manage RouterPorts using Class-based Formset'},
                      {'url':'customers','table_name':'Switches'},
                      {'url':'ras','table_name':'Remote Access Servers'})
        self.assertEqual(response.context[0].dicts[1]['table_list'], table_list)
        self.assertEqual(response.context[0].dicts[1]['title'], 'Table List')
        self.assertEqual(response.context[0].dicts[1]['user'], self.user)

    def test_router_details(self):
        """
        Test router details page
        """
        self.router = Router.objects.create(router_model="AL", last_maintained_date=datetime.datetime(2013, 07, 16, 13, 9, 25, tzinfo=utc))
        # Issue a GET request.
        login_result = self.client.login(username='test_account', password='password')
        self.assertEqual(login_result, True)

        url = '/SampleISP/routers/{0:d}/'.format(self.router.id)
        response = self.client.get('/SampleISP/routers/{0:d}/'.format(self.router.id))
        # Check that the response is 200 OK.
        self.assertEqual(response.status_code, 200)

        # Check that the rendered context data has correct form class and object
        self.assertIn('ISP-R-AL',response.content)
        self.assertIsInstance(response.context_data['form'], RouterForm)
        self.assertEqual(response.context_data['router'], self.router)

class SplinterTests(LiveServerTestCase):

    @classmethod
    def setUpClass(cls):
        """
        Every test needs a browser.
        """
        cls.browser = Browser()
        super(SplinterTests, cls).setUpClass()

    @classmethod
    def tearDownClass(cls):
        cls.browser.quit()
        super(SplinterTests, cls).tearDownClass()

    @classmethod
    def login(cls,browser,url):
        browser.visit(url)
        sleep(1)
        browser.fill('username','admin')
        browser.fill('password','admin')
        browser.find_by_value("Log in").click()
        sleep(1)

    def test_update_router(self):
        # self.browser.visit('%s%s' % (self.live_server_url, '/admin/'))
        # sleep(1)
        # self.browser.fill('username','admin')
        # self.browser.fill('password','admin')
        # self.browser.find_by_value("Log in").click()
        # sleep(1)
        SplinterTests.login(self.browser, '%s%s' % (self.live_server_url, '/admin/'))
        self.router = Router.objects.get(pk=1)
        url = '%s%s%d/' % (self.live_server_url, '/SampleISP/routers/', self.router.id)
        self.browser.visit(url)
        sleep(1)
        self.browser.select("router_model","DL")
        self.browser.fill('last_maintained_date','2013-07-18 00:00:00')
        sleep(10)
