from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        table = self.browser.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

    def test_can_start_a_list_and_retrieve_it_later(self):

        # user goes to homepage
        self.browser.get('http://localhost:8000')

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
        time.sleep(1)
        self.check_for_row_in_list_table('1. item 1')

        # user continues to see textbox inviting to add more. Enters 'item 2'
        inputbox = self.browser.find_element_by_id('id_new_item')
        inputbox.send_keys('item 2')
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # user sees both items on superlists
        self.check_for_row_in_list_table('1: item 1')
        self.check_for_row_in_list_table('2: item 2')

        # user notices site displays unique url for her

        # user visits unique url and sees both items on list


        self.fail('finish the tests')

if __name__ == '__main__':
    unittest.main(warnings='ignore')

browser.quit()
