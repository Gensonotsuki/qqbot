import json
import os

from nonebot import on_command, CommandSession
from nonebot import on_natural_language, NLPSession, NLPResult

from config import GROUP_LIST, HERO_NICKNAME

__plugin_name__ = HERO_NICKNAME

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = curPath[:curPath.find("qqbot\\") + len("qqbot\\")]

nickname = os.path.abspath(rootPath + '\\nickname.json')
e7_hero_decode = json.load(open(nickname, 'r'))


@on_natural_language(only_to_me=False)
async def _(session: NLPSession):
    global nickname, e7_hero_decode
    if session.ctx.get('group_id') not in GROUP_LIST:
        return None
    res = None
    msg_box = session.msg.strip().split()
    if msg_box[0] == '添加外号':
        e7_hero_decode[msg_box[2]] = e7_hero_decode[msg_box[1]]
        res = NLPResult(100, 'add_nicname', {'message': '外号添加成功'})
        json.dump(e7_hero_decode, open(nickname, 'w'))
        return res
    elif msg_box[0] == '查看外号':
        hero_nick = e7_hero_decode[msg_box[1]]
        nickname_list = []
        for j in filter(lambda x: hero_nick == x[1], e7_hero_decode.items()):
            nickname_list.append(j[0])
        res = NLPResult(100, 'check_nicname', {'message': hero_nick + '：' + '，'.join(nickname_list)})
        return res
    elif msg_box[0] == '添加角色':
        heroCNname = msg_box[1]
        heroENname = msg_box[2]
        e7_hero_decode[heroCNname] = msg_box[2]
        res = NLPResult(100, 'add_name', {'message': heroCNname + ':' + heroENname + '添加成功'})
        json.dump(e7_hero_decode, open(nickname, 'w'))
        return res


@on_command('add_nicname', only_to_me=False)
async def _(session: CommandSession):
    rs = session.args['message']
    await session.send(rs)


@on_command('check_nicname', only_to_me=False)
async def _(session: CommandSession):
    rs = session.args['message']
    await session.send(rs)


@on_command('add_name', only_to_me=False)
async def _(session: CommandSession):
    rs = session.args['message']
    await session.send(rs)
