# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from selenium import webdriver
import unittest, time
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.support.wait import WebDriverWait

from apps.ninjas.models import Ninja

class EndToEnd(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super(EndToEnd, cls).setUpClass()
        cls.selenium = webdriver.Chrome()
        cls.selenium.implicitly_wait(5)
  
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(EndToEnd, cls).tearDownClass()

    # HOMEPAGE TESTS
    def test_displays_home_page(self):
        self.selenium.get(self.live_server_url)
        html = self.selenium.page_source
        self.assertIn('Challenge Accepted!', html)
    
    def test_user_can_get_to_registration_page(self):
        self.selenium.get(self.live_server_url)
        registration_link = self.selenium.find_element_by_id('button-registration')
        registration_link.click()
        time.sleep(1)
        self.assertEqual(self.selenium.current_url, self.live_server_url + '/ninjas/register')
    
    # REGISTRATION PAGE TESTS
    def test_user_is_presented_with_registration_form(self):
        self.selenium.get(self.live_server_url + '/ninjas/register')
        registration_form = self.selenium.find_element_by_id('form-registration')
        self.assertEqual(registration_form.tag_name, 'form')
    
    def test_user_is_redirected_to_dashboard_after_successful_registration(self):
        self.register_user()
        time.sleep(2)
        self.assertEqual(self.selenium.current_url, self.live_server_url + '/ninjas/dashboard')
    
    # LOGIN PAGE TESTS
    def test_user_is_presented_with_login_form(self):
        self.selenium.get(self.live_server_url + '/ninjas/login')
        login_form = self.selenium.find_element_by_id('form-login')
        self.assertEqual(login_form.tag_name, 'form')
    
    def test_user_is_redirected_to_dashboard_after_successful_login(self):
        bob = Ninja.objects.validate_registration({
            'username': 'bob',
            'email': 'bob@email.com',
            'password': 'aGreatPassword123',
            'password_confirm': 'aGreatPassword123'
        })
        # TODO: Think about: how come this doesn't work if register_user is called,
        # and then the following code is run?
        self.selenium.get(self.live_server_url + '/ninjas/login')
        form = self.selenium.find_element_by_id('form-login')
        form.find_element_by_name('username').send_keys('bob')
        form.find_element_by_name('password').send_keys('aGreatPassword123')
        form.find_element_by_tag_name('button').click()
        time.sleep(2)
        self.assertEqual(self.selenium.current_url, self.live_server_url + '/ninjas/dashboard')

    def register_user(self):
        self.selenium.get(self.live_server_url + '/ninjas/register')
        form = self.selenium.find_element_by_id('form-registration')
        form.find_element_by_name('username').send_keys('bob')
        form.find_element_by_name('email').send_keys('bob@email.com')
        form.find_element_by_name('password').send_keys('aGreatPassword123')
        form.find_element_by_name('password_confirm').send_keys('aGreatPassword123')
        form.find_element_by_tag_name('button').click()