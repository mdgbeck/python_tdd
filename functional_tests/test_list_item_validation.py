from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def get_error_element(self):
        return self.browser.find_element_by_css_selector('.has-error')



    def test_cannot_add_duplicate_items(self):
        # user goes to start a new list
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys("repeat 1")
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: repeat 1")

        # user accidently tries to enter a duplicate item
        self.get_item_input_box().send_keys('repeat 1')
        self.get_item_input_box().send_keys(Keys.ENTER)

        # user sees a helpful error message
        self.wait_for(lambda: self.assertEqual(
            self.get_error_element().text,
            "You've already got this in your list"
        ))


    def test_cannot_add_empty_list_items(self):
        # user 1 got to home page and accidently adds a blank item
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys(Keys.ENTER)

        # page refreshes, gives error saying list item cannot be blank
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:invalid'
        ))

        # tries again with text in field and error disapperats
        self.get_item_input_box().send_keys('item 1')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:valid'
        ))

        # can submit
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: item 1')

        # stupidly, user tries another blank item
        self.get_item_input_box().send_keys(Keys.ENTER)

        # receives a similar warning
        self.wait_for_row_in_list_table('1: item 1')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:invalid'
        ))

        # she can correct by filling in some text
        self.get_item_input_box().send_keys('not blank')
        self.wait_for(lambda: self.browser.find_elements_by_css_selector(
            '#id_text:valid'
        ))
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: item 1')
        self.wait_for_row_in_list_table('2: not blank')


    def test_error_messages_are_cleared_on_input(self):

        # user starts a list and causes a validation error
        self.browser.get(self.live_server_url)
        self.get_item_input_box().send_keys('repeat')
        self.get_item_input_box().send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: repeat')
        self.get_item_input_box().send_keys('repeat')
        self.get_item_input_box().send_keys(Keys.ENTER)

        self.wait_for(lambda: self.assertTrue(
            self.get_error_element().is_displayed()
        ))

        # user starts typing in input box to clear error
        self.get_item_input_box().send_keys('a')

        # user sees error go away
        self.wait_for(lambda: self.assertFalse(
            self.get_error_element().is_displayed()
        ))
