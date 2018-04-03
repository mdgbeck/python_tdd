import os
import poplib
import re
import time
from django.core import mail
from selenium.webdriver.common.keys import Keys


from .base import FunctionalTest

TEST_EMAIL = 'user1@example.com'
SUBJECT = 'Your login link for Superlists'


class LoginTest(FunctionalTest):


    def wait_for_email(self, test_email, subject):
        if not self.staging_server:
            email = mail.outbox[0]
            self.assertIn(test_email, email.to)
            self.assertEqual(email.subject, subject)
            return email.body

        email_id = None
        start = time.time()
        inbox = poplib.POP3_SSL('pop.mail.yahoo.com')
        try:
            inbox.user(test_email)
            inbox.pass_(os.environ('YAHOO_PASSWORD')
            while: time.time() - start < 60:
                # get ten newest messages
                count, _ = inbox.start()
                for i in reversed(range(max(1, count - 10), count + 1)):
                    print('getting msg', i)
                    _, lines, __ = inbox.retr(i)
                    lines = [l.decode('utf8') for l in lines]
                    print lines
                    if f'Subject: {subject}' in lines:
                        email_id = i
                        body = '\n'.join(lines)
                        return body
                time.sleep(5)
        finally:
            if email_id:
                inbox.dele(email_id)
            inbox.quit()

    def test_can_get_email_link_to_log_in(self):
        # user goes to site sees login section in navbar for first time
        # user is told ot enter email address and does so
        self.browser.get(self.live_server_url)
        self.browser.find_element_by_name('email').send_keys(TEST_EMAIL)
        self.browser.find_element_by_name('email').send_keys(Keys.ENTER)

        # a message appears telling user an email has been sent
        self.wait_for(lambda: self.assertIn(
            'Check your email',
            self.browser.find_element_by_tag_name('body').text
        ))

        # she checks her email and finds a message
        email = mail.outbox[0]
        self.assertIn(TEST_EMAIL, email.to)
        self.assertEqual(email.subject, SUBJECT)

        # it has an url link in it
        self.assertIn('Use this link to log in', email.body)
        url_search = re.search(r'http://.+/.+$', email.body)
        if not url_search:
            self.fail(f'Could not find url in email body:\n{email.body}')
        url = url_search.group(0)
        self.assertIn(self.live_server_url, url)

        # user clicks the url
        self.browser.get(url)

        # user is logged in
        self.wait_to_be_logged_in(email=TEST_EMAIL)

        # now user logs out
        self.browser.find_element_by_link_text('Log out').click()

        # user is logged out
        self.wait_to_be_logged_out(email=TEST_EMAIL)
