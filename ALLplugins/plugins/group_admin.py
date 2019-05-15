from nonebot import on_request, RequestSession

from config import GROUP_LIST, GROUP_ADMIN


@on_request('group')
async def _(session: RequestSession):
    print(session.ctx)
    if session.ctx['group_id'] in GROUP_LIST:
        await session.approve()
        user_id = session.ctx['user_id']
        await session.send(GROUP_ADMIN + f'[CQ:at,qq={user_id}]')