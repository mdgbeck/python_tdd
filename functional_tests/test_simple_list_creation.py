from .base import FunctionalTest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(FunctionalTest):


    def test_can_start_a_list_for_one_user(self):

        # user goes to homepage
        self.browser.get(self.live_server_url)

        # user sees to do in title
        self.assertIn('To-Do', self.browser.title)
        header_text = self.browser.find_element_by_tag_name('h1').text
        self.assertIn('To-Do', header_text)

        # user is invited to add to do item
        inputbox = self.get_item_input_box()
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
        inputbox = self.get_item_input_box()
        inputbox.send_keys('item 2')
        inputbox.send_keys(Keys.ENTER)

        # user sees both items on list
        self.wait_for_row_in_list_table('2: item 2')
        self.wait_for_row_in_list_table('1: item 1')

        # user goes to sleep

    def test_multiple_users_can_start_lists_at_different_urls(self):

        # user starts a new to-do lists
        self.browser.get(self.live_server_url)
        inputbox = self.get_item_input_box()
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
        inputbox = self.get_item_input_box()
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
