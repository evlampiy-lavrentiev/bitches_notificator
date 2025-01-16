import asyncio
import logging
import telethon
from dateutil import tz
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

def construct_msg_text(id, username_info, date, action):
    act_str = ""
    if type(action) == telethon.types.ChannelAdminLogEventActionParticipantLeave:
        act_str = "Leave"
    elif type(action) == telethon.types.ChannelAdminLogEventActionParticipantJoin:
        act_str = "Join"

    date = date.astimezone(tz.gettz(get_variable('timezone')))

    name = username_info['name']
    username = username_info['username']
    logging.info(f'{id=} {username=} {name=}')
    if username is not None:
        link = f"t.me/{username}"
    else:
        link = f"tg://user?id={id}"
    return f'<a href=\"{link}\">{name}</a> <b>{act_str}</b> at {date}'

def get_usernames_dict(users):
    ans = dict()
    for user in users:
        ans[user.id] = {
            'name': (str(user.first_name or '') + ' ' + str(user.last_name or '')).strip(),
            'username': user.username
        }
    return ans


async def main():
    await create_sessions()

    admin = await bot.get_entity(get_variable('admin_id'))

    sended_messages = set()
    send_queue = []

    while True:
        logging.info("Begin iteration")
        actions = await get_recent_actions(client)
        id_to_username = get_usernames_dict(actions.users)
        for event in actions.events:
            username_info = id_to_username[event.user_id]
            send_queue.append(construct_msg_text(event.user_id, username_info, event.date, event.action))

        logging.info(f'{len(send_queue)=} {len(sended_messages)=}')
        for msg in send_queue:
            if msg in sended_messages:
                continue
            logging.info(f'sending message {msg}')
            await bot.send_message(admin, msg, parse_mode='html', link_preview=False)
            await asyncio.sleep(0.1)
            sended_messages.add(msg)

        send_queue.clear()


        one_h = 60 * 60
        await asyncio.sleep(24 * one_h)
        # await asyncio.sleep(10) # for debug

if __name__ == '__main__':
    asyncio.run(main())
    # bot.run_until_disconnected()