import json
import operator
import os

from nonebot.permission import SUPERUSER, GROUP_ADMIN
from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, IntentCommand

from ALLplugins.plugins.ep7crawl import push_article
from config import GONG_GAO_2, GONG_GAO_1, MANUAL_UPDATE_1, MANUAL_UPDATE_2, MANUAL_UPDATE_3, ANNOUCEMENT_NAME

from .data_source import get_annoucement

__plugin_name__ = ANNOUCEMENT_NAME

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = curPath[:curPath.find("qqbot\\") + len("qqbot\\")]

noticePath = os.path.abspath(rootPath + '\\notice.json')


@on_command('e7news', aliases=('公告'), only_to_me=False)
async def e7news(session: CommandSession):
    world = await get_act_title()
    wtsact = session.get('wtsact', prompt=world)
    act_text = await get_act(wtsact)
    await session.send(act_text)
    return act_text


# 收到公告命令后进入等待态，执行后续
@e7news.args_parser
async def _(session: CommandSession):
    stripped_arg = session.current_arg_text.strip()
    if session.is_first_run:
        if stripped_arg:
            session.state['wtsact'] = stripped_arg
        return
    if not stripped_arg:
        session.pause(GONG_GAO_2)
    session.state[session.current_key] = stripped_arg


# 查询数据库，返回最近公告列表
async def get_act_title() -> str:
    notice = json.load(open(noticePath, 'r'))
    res = sorted(notice, key=operator.itemgetter('article_id'), reverse=True)
    title_list = ''
    No = 1
    for i in res:
        try:
            title_list += (str(No) + '、' + i['article_title'] + '\t' + i['up_time'] + '\n')
        except:
            title_list += (str(No) + '、' + i['article_title'] + '\n')
        No += 1

    return GONG_GAO_1 + f'{title_list}'


async def get_act(numbuer) -> str:
    notice = json.load(open(noticePath, 'r'))
    res = sorted(notice, key=operator.itemgetter('article_id'), reverse=True)
    article = res[int(numbuer) - 1]['article']
    return f'{article}'


@on_natural_language(keywords={'公告'})
async def _(session: NLPSession):
    return IntentCommand(100, 'e7news')


@on_natural_language(keywords={'更新论坛'}, permission=SUPERUSER | GROUP_ADMIN)
async def _(session: NLPSession):
    return IntentCommand(100, 'forceFix')


@on_command('forceFix', aliases='更新论坛', only_to_me=False)
async def _(session: CommandSession):
    await session.send(MANUAL_UPDATE_1)
    notice = json.load(open(noticePath, 'r'))
    res = sorted(notice, key=operator.itemgetter('article_id'), reverse=True)
    article = push_article(notice)
    if not article:
        await session.send(MANUAL_UPDATE_2)
        return
    local_news_title = [i['article_title'] for i in res]
    bbs_article_title = [i['article_title'] for i in article]
    new_article_title = set(bbs_article_title) - set(local_news_title)
    for i in reversed(article):
        notice.insert(0, i)
    json.dump(notice, open(noticePath, 'w'))
    await session.send(MANUAL_UPDATE_3 + '\n'.join(new_article_title))
