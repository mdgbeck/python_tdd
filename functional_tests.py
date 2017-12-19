from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Check out homepage
        self.browser.get('http://localhost:8000')

        # notice to-do in title and header
        self.assertIn('To-Do', self.browser.title)
        self.fail('Finish the test!')

        # ivited to enter a to-do item straight away

        # types item 'buy money' into text box

        # page updated and displays
        # '1: buy money' as an item in a to-do list

        # text box inviting to add another item still exists
        # types 'use money'

        # page updates and shows both items

        # site has generated unique url and some explanatory text displays

        # visits the url and list is still displayed

        # generated

if __name__ == '__main__':
    unittest.main(warnings='ignore')
