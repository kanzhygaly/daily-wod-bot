import re
from datetime import datetime, date

from selenium.common.exceptions import NoSuchElementException

from bot.constants.page_fields import ELEMENT_NOT_FOUND_MSG, WOD_CONTENT_ID, TODAY_WOD_BTN_NAME
from bot.spider.lean_web_driver import LeanWebDriver


def parse_wod_date(driver: LeanWebDriver) -> date:
    """
    Parse WOD date from a page

    :param driver:
    :return:
    - WOD date
    """

    main_section = driver.find_element_by_tag_name('main')
    date_element = main_section.find_element_by_tag_name('time')
    return datetime.fromisoformat(date_element.get_attribute('datetime')).date()


def parse_wod_url(driver: LeanWebDriver) -> str:
    """
    Parse WOD link from a page

    :param driver:
    :return:
    - Link to WOD page
    """
    wod_url = None

    header_section = driver.find_element_by_tag_name('article')
    wod_links = header_section.find_elements_by_tag_name('a')

    for link in wod_links:
        link_text = re.sub('[^A-Za-z0-9]+', '', link.text.lower())
        if TODAY_WOD_BTN_NAME in link_text:
            wod_url = link.get_attribute('href')
            break

    if not wod_url:
        main_section = driver.find_element_by_tag_name('main')
        wod_url = main_section.find_element_by_tag_name('a').get_attribute('href')

    return wod_url


def parse_wod_content(driver: LeanWebDriver) -> str:
    """
    Parse WOD content from a page

    :param driver:
    :return:
    - WOD text formatted to Markdown style
    """
    output = ''

    content = driver.find_element_by_id(WOD_CONTENT_ID)
    paragraphs = content.find_elements_by_tag_name('p')

    for p in paragraphs:
        paragraph = ''

        try:
            img = p.find_element_by_tag_name('img')
            href = img.get_attribute('src')
            paragraph += href
        except NoSuchElementException:
            pass

        try:
            iframe = p.find_element_by_tag_name('iframe')
            title = iframe.get_attribute('title')
            href = iframe.get_attribute('src')
            paragraph += f'[{title}]({href})'
        except NoSuchElementException:
            pass

        try:
            link = p.find_element_by_tag_name('a')
            link_text = link.text
            link_href = link.get_attribute('href')
            if not link_text:
                link_text = ELEMENT_NOT_FOUND_MSG
                paragraph += link_href
        except NoSuchElementException:
            link_text = ELEMENT_NOT_FOUND_MSG
            link_href = ''

        try:
            bold = p.find_element_by_tag_name('strong')
            bold_text = bold.text
        except NoSuchElementException:
            bold_text = ELEMENT_NOT_FOUND_MSG

        paragraph += p.text + '\n'

        # escape special characters
        paragraph = paragraph.replace('*', '\\*').replace('`', '\\`')

        # convert to Markdown style
        if bold_text != ELEMENT_NOT_FOUND_MSG:
            paragraph = paragraph.replace(bold_text, f'*{bold_text}*')
        if link_text != ELEMENT_NOT_FOUND_MSG:
            paragraph = paragraph.replace(link_text, f'[{link_text}]({link_href})')

        output += paragraph + '\n'

    return output


