import asyncio
import logging
import telethon
import tz
from config import get_variable

logger = logging.getLogger('bitches')
ch = logging.StreamHandler()
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger.setLevel(logging.INFO)
logging = logger
logging.info('Init logger')

SESSION_PATH = "sessions/admin"
BOTSESSION_PATH = "sessions/bot"

channel = None
client, bot = None, None

async def create_sessions():
    global client
    global bot
    client = telethon.TelegramClient(SESSION_PATH,
                            get_variable('api_id'),
                            get_variable('api_hash')
                            )
    bot = telethon.TelegramClient(BOTSESSION_PATH,
                            get_variable('api_id'),
                            get_variable('api_hash')
                            )

    await client.start()
    await bot.start(bot_token=get_variable('bot_token'))
 

async def get_recent_actions(client):
    global channel
    if channel is None:
        # channel_id = -1001468868311
        # channel = await client.get_entity(telethon.tl.types.PeerChannel(channel_id))
        channel = await client.get_entity(get_variable('channel_id'))

    recent_actions = await client(telethon.functions.channels.GetAdminLogRequest(
        channel=channel,
        limit = 100,
        q = '',
        min_id = 0,
        max_id = 0,
        events_filter=telethon.tl.types.ChannelAdminLogEventsFilter(
            join=True,
            leave=True,
        )
    ))
    return recent_actions

def construct_msg_text(id, username, date, action):
    act_str = ""
    if type(action) == telethon.types.ChannelAdminLogEventActionParticipantLeave:
        act_str = "Leave"
    elif type(action) == telethon.types.ChannelAdminLogEventActionParticipantJoin:
        act_str = "Join"
    
    date = date.astimezone(tz.gettz(get_variable('timezone')))
    
    return f'<a href=\"tg://user?id={id}\">{username}</a> <b>{act_str}</b> in {date}'
    #     await my_client.client.send_message(
    #     my_client.chat_entity, 
    #     f'<a href=\"tg://user?id={ent.user_id}\">{mentioned_name}</a> карта (пинг через {timeout_sec} секунд)',
    #     reply_to=event.message,
    #     parse_mode='html'
    # )
    

def get_username_str(event):
    for user in event.users:
        return (str(user.first_name or '') + ' ' + str(user.last_name or '')).strip()


async def main():
    await create_sessions()

    admin = await bot.get_entity(get_variable('admin_id'))

    sended_messages = set()
    send_queue = []

    while True:
        logging.info("Begin iteration")
        logres = await get_recent_actions(client)
        for event in logres.events:
            username = get_username_str(event)
            send_queue.append(construct_msg_text(event.user_id, username, event.date, event.action))

        logging.info(f'{len(send_queue)=} {len(sended_messages)=}')
        for msg in send_queue:
            if msg in sended_messages:
                continue
            logging.info(f'sending message {msg}')
            await bot.send_message(admin, msg, parse_mode='html')
            await asyncio.sleep(0.1)
            sended_messages.add(msg)

        send_queue.clear()


        one_h = 60 * 60
        await asyncio.sleep(24 * one_h)
        # await asyncio.sleep(10) # for debug

if __name__ == '__main__':
    asyncio.run(main())
    # bot.run_until_disconnected()