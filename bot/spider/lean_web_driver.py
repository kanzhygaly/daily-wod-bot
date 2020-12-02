from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver


class LeanWebDriver(WebDriver):

    def __init__(self):
        options = Options()
        options.headless = True  # Runs Chrome in headless mode.
        options.add_argument('--no-sandbox')  # Bypass OS security model
        options.add_argument('--disable-gpu')  # applicable to windows os only
        options.add_argument('disable-infobars')
        options.add_argument("--disable-extensions")

        super().__init__(
            # executable_path='/Users/yerlan.akhmetov/Documents/selenium/chromedriver',
            options=options
        )
