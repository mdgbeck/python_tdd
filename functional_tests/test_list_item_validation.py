from selenium.webdriver.common.keys import Keys
from unittest import skip
from .base import FunctionalTest


class ItemValidationTest(FunctionalTest):

    def test_cannot_add_empty_list_items(self):
        # user 1 got to home page and accidently adds a blank item

        # page refreshes, gives error saying list item cannot be blank

        # tries again with text in field, works

        # stupidly, user tries another blank item

        # receives a similar warning

        # she can correct by filling in some text

        self.fail('write test')
