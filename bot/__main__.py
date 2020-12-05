import os
import time

from bot.db.db_client import DbClient
from bot.db.repository import Repository
from bot.dto.dto import PageDto, UserDto, DbCredentials
from bot.models.models import WOD, Provider
from bot.spider.selenium_spider import SeleniumSpider

URL = os.environ['BASE_URL']
LOGIN_PATH = os.environ['LOGIN_PATH']
LOGIN = os.environ['LOGIN']
PASSWORD = os.environ['PASSWORD']
DB_CREDENTIALS = DbCredentials.from_string(os.environ['DATABASE_URL'])

if __name__ == '__main__':
    db_client = DbClient(DB_CREDENTIALS)
    repo = Repository(db_client)

    start_time = time.time()
    spider = SeleniumSpider(
        page=PageDto(url=URL, login_path=LOGIN_PATH),
        user=UserDto(login=LOGIN, password=PASSWORD)
    )
    print("--- %s seconds ---" % (time.time() - start_time))

    print(spider.get_wod_title())
    print(spider.get_wod_content())

    provider = repo.get_one_by_entity(Provider(name='Misfit Athletics'))
    wod = WOD(
        wod_day=spider.get_wod_date(),
        title=spider.get_wod_title(),
        content=spider.get_wod_content(),
        provider_id=provider.provider_id
    )
    wod.save(repo)
