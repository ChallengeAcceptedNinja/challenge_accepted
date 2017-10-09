# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from selenium import webdriver
import unittest
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.support.wait import WebDriverWait

class HomePageTest(StaticLiveServerTestCase):
    @classmethod
    def setUpClass(cls):
        super(HomePageTest, cls).setUpClass()
        cls.selenium = webdriver.Chrome()
        cls.selenium.implicitly_wait(10)
  
    @classmethod
    def tearDownClass(cls):
        cls.selenium.refresh()
        cls.selenium.quit()
        super(HomePageTest, cls).tearDownClass()

    def test_displays_coming_soon_page(self):
        self.selenium.get(self.live_server_url)
        html = self.selenium.page_source
        self.assertIn('Coming soon', html)