from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # user 1 got to home page and accidently adds a blank item
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        # page refreshes, gives error saying list item cannot be blank
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "You can't have an empty list item"
        ))

        # tries again with text in field, works
        self.browser.find_element_by_id('id_new_item').send_keys('item 1')
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: item 1')

        # stupidly, user tries another blank item
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)

        # receives a similar warning
        self.wait_for(lambda: self.assertEqual(
            self.browser.find_element_by_css_selector('.has-error').text,
            "You can't have an empty list item"
        ))

        # she can correct by filling in some text
        self.browser.find_element_by_id('id_new_item').send_keys('not blank')
        self.browser.find_element_by_id('id_new_item').send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table('1: item 1')
        self.wait_for_row_in_list_table('2: not blank')

        self.fail('finish this test')
