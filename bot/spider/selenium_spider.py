from datetime import date

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from bot.constants.page_fields import LOGIN_FIELD_ID, PASSWORD_FIELD_ID, LOGIN_BUTTON_ID, EC_PROFILE_ELEMENT, \
    WOD_CONTENT_ID, EC_ALL_WODS_ELEMENT
from bot.dto.dto import PageDto, UserDto
from bot.spider.lean_web_driver import LeanWebDriver
from bot.spider.selenium_parser import parse_wod_content, parse_wod_url, parse_wod_date


class SeleniumSpider:

    def __init__(self, page: PageDto, user: UserDto):
        self.__driver = LeanWebDriver()

        try:
            self.__driver.get(page.get_login_url())
            try:
                self.__submit_login(user.login, user.password)
            except TimeoutException:
                self.__submit_login(user.login, user.password)

            self.__go_to_page(url=page.url, condition=(By.CLASS_NAME, EC_ALL_WODS_ELEMENT))

            self.__wod_date = parse_wod_date(self.__driver)

            # 'December 1, 2020' date format
            self.__wod_title = '{0:%B} {0.day}, {0:%Y}'.format(self.__wod_date)

            wod_url = parse_wod_url(self.__driver)

            self.__go_to_page(url=wod_url, condition=(By.ID, WOD_CONTENT_ID))

            self.__wod_content = parse_wod_content(self.__driver)
        finally:
            self.__driver.quit()

    def get_wod_date(self) -> date:
        return self.__wod_date

    def get_wod_title(self) -> str:
        return self.__wod_title

    def get_wod_content(self) -> str:
        return self.__wod_content

    def __submit_login(self, login: str, password: str):
        self.__driver.find_element_by_id(LOGIN_FIELD_ID).send_keys(login)
        self.__driver.find_element_by_id(PASSWORD_FIELD_ID).send_keys(password)
        self.__driver.find_element_by_id(LOGIN_BUTTON_ID).click()
        WebDriverWait(self.__driver, 10).until(
            expected_conditions.presence_of_element_located((By.ID, EC_PROFILE_ELEMENT))
        )

    def __go_to_page(self, url, condition):
        self.__driver.get(url)
        WebDriverWait(self.__driver, 10).until(
            expected_conditions.presence_of_element_located(condition)
        )
