import json
import operator
import os
import time
from datetime import datetime

import nonebot
import pytz
from aiocqhttp.exceptions import Error as CQHttpError
from ALLplugins.plugins.ep7crawl import push_article
from config import GROUP_ID, MANUAL_UPDATE_3, REMIND

__plugin_name__ = '会战前一天晚上进行配置提醒\n自动转发论坛'
bot = nonebot.get_bot()

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = curPath[:curPath.find("qqbot\\") + len("qqbot\\")]

noticePath = os.path.abspath(rootPath + '\\notice.json')



# 每周2,4,星期天晚上11点半提醒团战配置
@nonebot.scheduler.scheduled_job('cron', day_of_week='1,3,6', hour=23, minute=30, jitter=30, timezone='Asia/Shanghai')
async def _():
    global bot
    try:
        await bot.send_group_msg(group_id=GROUP_ID,
                                 message=REMIND)

    except CQHttpError:
        pass


@nonebot.scheduler.scheduled_job('cron',
                                 day_of_week=2,
                                 hour='14-22',
                                 minute='0,5,10,15,20,25,30,35,40,45,50,55',
                                 jitter=30, timezone='Asia/Shanghai')
async def _():
    global bot,noticePath
    notice = json.load(open(noticePath, 'r'))
    res = sorted(notice, key=operator.itemgetter('article_id'), reverse=True)
    local_news_title = [i['article_title'] for i in res]
    print(local_news_title)
    latest_news = push_article(res)
    if latest_news:
        bbs_article_title = [i['article_title'] for i in latest_news]
        new_article_title = set(bbs_article_title) - set(local_news_title)
        print(local_news_title)
        try:
            await bot.send_group_msg(group_id=GROUP_ID,
                                     message=MANUAL_UPDATE_3 + '\n'.join(new_article_title))
            for i in reversed(latest_news):
                notice.insert(0, i)
            json.dump(notice, open(noticePath, 'w'))
        except CQHttpError:
            pass
    time.sleep(30)

    # e7news = e7news_set.find().sort('article_id', -1).limit(10)
    # local_news_title = [i['article_title'] for i in e7news]


@nonebot.scheduler.scheduled_job('cron',
                                 day_of_week='0, 1, 3, 4, 5, 6',
                                 hour='8-18',
                                 minute='0,30',
                                 jitter=40, timezone='Asia/Shanghai')
async def _():
    global bot,noticePath
    notice = json.load(open(noticePath, 'r'))
    res = sorted(notice, key=operator.itemgetter('article_id'), reverse=True)
    local_news_title = [i['article_title'] for i in res]
    print(local_news_title)
    latest_news = push_article(res)
    if latest_news:
        bbs_article_title = [i['article_title'] for i in latest_news]
        new_article_title = set(bbs_article_title) - set(local_news_title)
        print(local_news_title)
        try:
            await bot.send_group_msg(group_id=GROUP_ID,
                                     message=MANUAL_UPDATE_3 + '\n'.join(new_article_title))

        except CQHttpError:
            pass
        for i in reversed(latest_news):
            notice.insert(0, i)
        json.dump(notice, open(noticePath, 'w'))
    time.sleep(30)
