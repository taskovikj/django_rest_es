import time

from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver import Keys


class HostTest(LiveServerTestCase):
    def test_home_page(self):
        driver = webdriver.Chrome()

        driver.get('http://127.0.0.1:8000/')
        assert "BlogPost" in driver.title

    def test_registration_and_redirection(self):
        driver = webdriver.Chrome()
        driver.get('http://127.0.0.1:8000/register')  # Replace with your app's registration URL

        # Find registration form elements
        username_input = driver.find_element('name', 'username')
        email_input = driver.find_element('name', 'email')
        password1_input = driver.find_element('name', 'password1')
        password2_input = driver.find_element('name', 'password2')

        # Enter registration details
        username_input.send_keys('testuser99')
        email_input.send_keys('tasdasd@example.com')
        password1_input.send_keys('securepassword223.')
        password2_input.send_keys('securepassword223.')

        button = driver.find_element('name', 'submit')
        driver.execute_script("arguments[0].click();", button)

        # Wait for registration to complete and check if we are redirected to the login page
        time.sleep(3)

        # Assert that we are on the login page after successful registration
        assert 'Login' in driver.page_source

    # def login_test(self):
    #     driver = webdriver.Chrome()
    #     driver.get('http://127.0.0.1:8000/login')
    #
    #     username_input = driver.find_element('name', 'username')
    #     password_input = driver.find_element('name', 'password')
    #
    #     username_input.send_keys('admin')
    #     password_input.send_keys('admin')
    #
    #     password_input.send_keys(Keys.RETURN)
    #
    #     time.sleep(3)
    #
    #     redirect_url = driver.current_url
    #     expected_url = 'http://localhost:8000/'
    #     assert redirect_url == expected_url, f"Expected redirect URL: {expected_url}, Actual URL: {redirect_url}"




print("Test Execution Started")

# Initialize Chrome WebDriver with custom options
options = webdriver.ChromeOptions()
options.add_argument('--ignore-ssl-errors=yes')
options.add_argument('--ignore-certificate-errors')

try:
    # Initialize the WebDriver
    driver = webdriver.Remote(
        command_executor='http://localhost:4444/wd/hub',
        options=options
    )

    # Maximize the window size
    driver.maximize_window()
    time.sleep(10)

    # Navigate to browserstack.com
    driver.get("https://www.browserstack.com/")
    time.sleep(10)

    # Click on the "Get started for free" button
    driver.find_element("link text", "Get started free").click()
    time.sleep(10)

    # Second test
    ht = HostTest()
    ht.test_home_page()

    # Test registration and redirection
    ht.test_registration_and_redirection()

    # ht.login_test()

except Exception as e:
    # Handle exceptions here, you can log the exception if needed
    print(f"Exception occurred: {str(e)}")

finally:
    # Ensure that the WebDriver server is quit even if an exception occurs
    if 'driver' in locals() or 'driver' in globals():
        try:
            driver.close()
            driver.quit()
        except Exception as e:
            # Handle any exception that might occur while quitting the driver
            print(f"Exception occurred during driver quit: {str(e)}")

print("Test Execution Completed!")
