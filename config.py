import re
from datetime import timedelta
from nonebot.default_config import *

SUPERUSERS = {}  # 这里面填机器人管理员qq号
HOST = '0.0.0.0'
PORT = 8080
NICKNAME = ['cb']  # 这里面填机器人名字,下面的也要改成一样的
COMMAND_START = ['cb', re.compile(r'[\!]+')]
DEBUG = True
SESSION_RUN_TIMEOUT = timedelta(seconds=10)
DEFAULT_VALIDATION_FAILURE_EXPRESSION = '指令格式有误，请检查'
GROUP_LIST = [123123123]  # 这里面填qq群
GROUP_ID = 123123123
# 这是功能区提示话,可根据需求更改,结尾的\n为换行符
ANNOUCEMENT_NAME = '*官方论坛公告查询，输入‘cb公告’'
GONG_GAO_1 = '*官方论坛最新公告,请回复数字查看详情~\n'
GONG_GAO_2 = '*要查询的公告编号不能为空[CQ:face,id=74][CQ:face,id=74]'
MANUAL_UPDATE_1 = '请稍等，该过程会比较慢'
MANUAL_UPDATE_2 = '暂时没有更新新闻哦，请稍后再尝试查询'
MANUAL_UPDATE_3 = '论坛有最新公告哟~请使用‘cb 公告’进行查询\n'
#提醒团战配置
REMIND='现在晚上11点半，配置团战的话赶紧配置了哦~[CQ:emoji,id=128522][CQ:emoji,id=128522][CQ:emoji,id=128522]'
GROUP_ADMIN='萌新们注意咯，有新大佬入群[CQ:emoji,id=127881]'

MAZA_CHAT_NAME = '*迷宫聊天查询器，输入‘cb 迷宫聊天“”’该功能支持外号查询'
CHAT_MENBER = '想在迷宫聊天的是哪四位呢[CQ:face,id=13]'
CHAT_ERROR = '似乎没有4个人呢[CQ:face,id=106]\n请用空格将其隔开'

HERO_NICKNAME = '*添加外号\t格式:cb添加外号 木飞 木飞剑\n*添加角色\t格式:cb添加角色 木飞 Iseria\n*查看外号\tcb查看外号 木飞'
