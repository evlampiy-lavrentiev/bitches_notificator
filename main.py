import json
import asyncio
import logging
import telethon
import time

logger = logging.getLogger('bitches')
ch = logging.StreamHandler()
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(filename)s:%(lineno)d - %(message)s",
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger.setLevel(logging.INFO)
logging = logger
logging.info('init logger')

user_id_to_notify = 532127924
channel_id = -1001468868311
channel = None
session_path = "sessions/amirkek"
botsession_path = "sessions/amirbot"

def load_credentials(credentials_path = 'credentials.json'):
    cred = json.load(open(credentials_path, 'r'))
    return cred


cred = load_credentials()
client = telethon.TelegramClient(session_path,
                            cred['api_id'],
                            cred['api_hash']
                            )
bot = telethon.TelegramClient(botsession_path,
                            cred['api_id'],
                            cred['api_hash']
                            )

async def start_sessions():
    global client
    global bot
    global cred

    await client.start()
    await bot.start(bot_token=cred['bot_token'])
 

async def get_recent_actions(client):
    global channel
    global channel_id
    if channel is None:
        # channel = await client.get_entity(telethon.tl.types.PeerChannel(channel_id))
        channel = await client.get_entity("@shizoshitt")

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

def construct_msg(username, id, date, action):
    act_str = ""
    if type(action) == telethon.types.ChannelAdminLogEventActionParticipantLeave:
        act_str = "LEAVE"
    elif type(action) == telethon.types.ChannelAdminLogEventActionParticipantJoin:
        act_str = "JOIN"

    return f'<a href=\"tg://user?id={id}\">{username}</a> <b>{act_str}</b> in {date}'
    #     await my_client.client.send_message(
    #     my_client.chat_entity, 
    #     f'<a href=\"tg://user?id={ent.user_id}\">{mentioned_name}</a> карта (пинг через {timeout_sec} секунд)',
    #     reply_to=event.message,
    #     parse_mode='html'
    # )
    

def extract_usernames(logres):
    ans = dict()
    for user in logres.users:
        ans[user.id] = (str(user.first_name or '') + ' ' + str(user.last_name or '')).strip()
    return ans


def setup_handlers():
    @bot.on(telethon.events.NewMessage(pattern='/recent_actions'))
    async def handler(event):
        if event.sender_id != user_id_to_notify:
            await event.reply('Go away')
        else:
            await event.reply('You are ok', parse_mode='html')
            time.sleep(10)
            await event.reply('You are ok', parse_mode='html')

async def main():
    await start_sessions()

    me = await bot.get_entity(user_id_to_notify)

    sended_messages = set()
    send_queue = []

    while True:
        logging.info("WAKEUP")
        logres = await get_recent_actions(client)
        id_to_username = extract_usernames(logres)
        for event in logres.events:
            send_queue.append(construct_msg(id_to_username[event.user_id], event.user_id, event.date, event.action))

        logging.info(f'{len(send_queue)=} {len(sended_messages)=}')
        for msg in [msg for msg in send_queue if msg not in sended_messages]:
            logging.info(f'sending message {msg}')
            await bot.send_message(me, msg, parse_mode='html')
            sended_messages.add(msg)

        send_queue.clear()


        one_h = 60 * 60
        await asyncio.sleep(24 * one_h)
        # await asyncio.sleep(10) # for debug

if __name__ == '__main__':
    asyncio.run(main())
    # bot.run_until_disconnected()