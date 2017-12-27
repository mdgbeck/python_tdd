from selenium import webdriver
import unittest

class NewVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):

        # user goes to homepage
        self.browser.get('http://localhost:8000')

        # user sees to do in title
        self.assertIn("To-Do", self.browser.title)
        self.fail('Finish the test!')

        # user is invited to add to do item

        # user types 'item 1' into text box

        # user hits enter and sees item 1 on list

        # user continues to see textbox inviting to add more. Enters 'item 2'

        # user sees both items on superlists

        # user notices site displays unique url for her

        # user visits unique url and sees both items on list

if __name__ == '__main__':
    unittest.main(warnings='ignore')

browser.quit()
