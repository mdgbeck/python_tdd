from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import  WebDriverException
import time

MAX_WAIT = 10

class NewVisitorTest(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                table = self.browser.find_element_by_id('id_list_table')
                rows = table.find_elements_by_tag_name('tr')
                self.assertIn(row_text, [row.text for row in rows])
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise # -*- coding: utf-8 -*-
                time.sleep(0.5)

    def test_can_start_a_list_for_one_user(self):

        # user goes to homepage
        self.browser.get(self.live_server_url)

        # user sees to do in title
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # user is invited to add to do item
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
        )

        # user types 'item 1' into text box
        inputbox.send_keys('item 1')

        # user hits enter and sees item 1 on list
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: item 1')

        # user continues to see textbox inviting to add more. Enters 'item 2'
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('item 2')
        inputbox.send_keys(Keys.ENTER)

        # user sees both items on list
        self.wait_for_row_in_list_table('2: item 2')
        self.wait_for_row_in_list_table('1: item 1')

        # user goes to sleep

    def test_multiple_users_can_start_lists_at_different_urls(self):

        # user starts a new to-do lists
        self.browser.get(self.live_server_url)
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('item 1')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: item 1')

        # user notices site displays unique url for her
        user_list_url = self.browser.current_url
        self.assertRegex(user_list_url, '/lists/.+')

        # a new user comes along ot the saved_items
        ## we use a new browser session to make sure that no info
        ## of user1 is coming from cookies, etc.
        self.browser.quit()
        self.browser = webdriver.Firefox()

        # user2 visits home page, no sign of user1 lists
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('item 1', page_text)
        self.assertNotIn('item 2', page_text)

        # user2 starts new list
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('letter a')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: letter a')

        # user2 gets his own unique url
        user2_list_url = self.browser.current_url
        self.assertRegex(user2_list_url, '/lists/.+')
        self.assertNotEqual(user2_list_url, user_list_url)

        # again no trace of user1 lists
        page_text = self.browser.find_element_by_tag_name('body').text
        self.assertNotIn('item 1', page_text)
        self.assertIn('letter a', page_text)

        # both go back to sleep

    def test_layout_and_styling(self):
        # User1 goes to the home page
        self.browser.get(self.live_server_url)
        self.browser.set_window_size(1024, 768)

        # user notices the input box is nicely centered
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta = 10
        )

        # user starts a new list and sees the input is nicely centered there too
        inputbox.send_keys('testing')
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: testing')
        inputbox = self.browser.find_element_by_id('id_new_item')
        self.assertAlmostEqual(
            inputbox.location['x'] + inputbox.size['width'] / 2,
            512,
            delta=10
        )
