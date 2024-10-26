import json
import asyncio
import logging
import telethon

logger = logging.getLogger('bitches')
ch = logging.StreamHandler()
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger.setLevel(logging.INFO)
logging = logger
logging.info('init logger')

allowed_user_id = [532127924]
channel_id = -1001468868311
channel = None
session_path = "sessions/amirkek"

def load_credentials(credentials_path = 'credentials.json'):
    cred = json.load(open(credentials_path, 'r'))
    return cred


cred = load_credentials()
client = telethon.TelegramClient(session_path,
                            cred['api_id'],
                            cred['api_hash']
                            )

async def get_recent_actions(bot):
    global channel
    logging.info(channel)
    if channel is None:
        logging.info('Getting channel entity')
        channel = await bot.get_entity(channel_id)

    recent_actions = await bot(telethon.tl.functions.channels.GetAdminLog(
        channel=channel,
        limit=100,  # количество записей
        events_filter=telethon.tl.types.ChannelAdminLogEventsFilter(
            join=True,
            leave=True,
            invite=True,
            promote=True,
            demote=True,
            info=True,
            settings=True,
            pinned=True,
            edit=True,
            delete=True
        )
    ))
    return recent_actions



# @bot.on(telethon.events.NewMessage(pattern='/recent_actions'))
# async def handler(event):
#     if event.sender_id not in allowed_user_id:
#         await event.reply('Go away')
    
#     await event.reply('You are OK')

async def main():
    global client

    logging.info('-1')
    # await client.run_until_disconnected()
    logging.info('0')
    # bot = await client.start(bot_token=cred['bot_token'])
    bot = await client.start()
    logging.info('1')
    res = await get_recent_actions(bot)
    logging.info('aboba)))')
    print(res)

if __name__ == '__main__':
    asyncio.run(main())
    # bot.run_until_disconnected()