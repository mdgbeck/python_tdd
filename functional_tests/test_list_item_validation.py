from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

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
