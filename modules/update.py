from cashews import cache

from glover import chat_id, username
from init import scheduler, bot, logs
from defs.search import search


# 15 分钟执行一次
@scheduler.scheduled_job("interval", minutes=15)
async def update():
    logs.info("开始检查新邮件")
    mails = await search()
    for m in mails:
        try:
            await m.send(bot, chat_id)
            await cache.set(f"mail:{username}:{m.id}", 1)
        except Exception as e:
            logs.exception("发送邮件失败", exc_info=e)
    logs.info("检查新邮件结束")


bot.loop.create_task(update())
