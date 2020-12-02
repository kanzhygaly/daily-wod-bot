import os
import time

from bot.dto.page_dto import PageDto
from bot.dto.user_dto import UserDto
from bot.spider.selenium_spider import SeleniumSpider

if __name__ == '__main__':
    url = os.environ['BASE_URL']
    login_path = os.environ['LOGIN_PATH']
    login = os.environ['LOGIN']
    password = os.environ['PASSWORD']

    start_time = time.time()

    spider = SeleniumSpider(
        page=PageDto(url=url, login_path=login_path),
        user=UserDto(login=login, password=password)
    )

    print(spider.get_wod_title())
    print(spider.get_wod_content())

    print("--- %s seconds ---" % (time.time() - start_time))
