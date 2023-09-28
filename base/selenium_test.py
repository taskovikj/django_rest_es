import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class HomePageTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def test_home_page(self):
        driver = self.driver
        driver.get('http://127.0.0.1:8000/')
        self.assertIn("BlogPost", driver.title)


class RegistrationTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def test_registration_and_redirection(self):
        driver = self.driver
        driver.get('http://127.0.0.1:8000/register')

        username_input = driver.find_element('name', 'username')
        email_input = driver.find_element('name', 'email')
        password1_input = driver.find_element('name', 'password1')
        password2_input = driver.find_element('name', 'password2')

        username_input.send_keys('testuser99')  # TODO: Enter username that does not exist in DB
        email_input.send_keys('tasdasd@example.com')
        password1_input.send_keys('securepassword223.')
        password2_input.send_keys('securepassword223.')

        button = driver.find_element('name', 'submit')
        driver.execute_script("arguments[0].click();", button)

        time.sleep(3)

        self.assertIn('Login', driver.page_source)


class LoginTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()

    def test_login(self):
        driver = self.driver
        driver.get('http://127.0.0.1:8000/login')

        username_input = driver.find_element('name', 'username')
        password_input = driver.find_element('name', 'password')

        username_input.send_keys('admin')  # TODO: Enter username and pw that already exist in DB
        password_input.send_keys('admin')

        password_input.send_keys(Keys.RETURN)

        time.sleep(3)

        redirect_url = driver.current_url
        expected_url = 'http://127.0.0.1:8000/'
        self.assertEqual(redirect_url, expected_url,
                         f"Expected redirect URL: {expected_url}, Actual URL: {redirect_url}")


if __name__ == "__main__":
    try:

        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-ssl-errors=yes')
        options.add_argument('--ignore-certificate-errors')

        # Run
        unittest.main(verbosity=2, exit=False)

    except Exception as e:
        print(f"Exception occurred: {str(e)}")
