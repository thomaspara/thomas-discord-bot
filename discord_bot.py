import discord
from std_server import std_manager
from power_manager import power_manager
from discord.ext import commands, tasks
import time
import schedule
import threading
import asyncio
import json

intents = discord.Intents.default()
intents.presences = True
intents.members = True
print(intents)
print("bot started")

f = open('config.json')
config = json.load(f)
f.close()
settings = config['settings']
server_configs = config['servers']

def remove_prefix(text, prefix):
    return text[text.startswith(prefix) and len(prefix):]


client = discord.Client(intents=intents)
summon = settings["summon_word"] + " "
srv_num = settings["max_servers"] # todo implement this
bot_channels = settings["bot_channels"] 

power = power_manager()
# make servers
server_list = []
for s in server_configs:
    server_list.append(std_manager(s['name'],s['screen_name'],s['cmd'],s['ip'],s['stop_word'],s['admin_role']))

# make help message
server_instr = ''
for server in server_list:
    server_instr += server.help + '\n\n'

help_msg = f'''to use me say `{summon.strip()}` 
I will ignore you outside of {bot_channels} or if you have the Bot Banned role
Commands:
{server_instr}`live` shows status of all servers
`ip` shows ip list
`help` shows this message'''

# make ip msg
server_ips = ''
for server in server_list:
    server_ips += server.ip + '\n'

ips = f'''server list
{server_ips}
Ask Thomas for help if you can't connect
'''


async def send_message_helper(channel, msg):
    await channel.send(msg)


def send_message(channels, msg):
    for channel in channels:
        client.loop.create_task(send_message_helper(channel, msg))

# make stops


def stop_all():
    rsp = ""
    for server in server_list:
        rsp += server.stop()
    return rsp


def scheduled_jobs():
    schedule.every().day.at("06:00").do(send_message, channels=bot_channels,
                                        msg="server rebooting, stopping all running servers")
    schedule.every().day.at("06:01").do(stop_all)
    schedule.every().day.at("06:06").do(power.reboot)

    print(schedule.jobs)


@tasks.loop(seconds=1)
async def run_scheduled_tasks():
    schedule.run_pending()


@client.event
async def on_ready():
    print("bot ready")
    for guild in client.guilds:
        for channel in guild.channels:
            if channel.name in bot_channels:
                bot_channels.append(channel)
    print(bot_channels)
    scheduled_jobs()
    run_scheduled_tasks.start()
    send_message(bot_channels, "bot online")
    judge_msg = ''


@client.event
async def on_message(message):
    if message.channel.name not in bot_channels:
        return
    if message.author == client.user:
        return
    if not message.content.startswith(summon.strip()):
        return
    roles = [r.name for r in message.author.roles]
    if "Bot Banned" in roles:
        return
    msg = message.content
    msg = msg.lower().strip()
    rsp = ''

    if summon.strip() == msg or f'{summon}help' == msg:
        rsp = help_msg
    # power management
    elif msg == f'{summon}reboot' and settings["super_admin"] in roles:
        power.reboot()
        rsp = "server rebooting"
    elif msg == f'{summon}shutdown' and settings["super_admin"] in roles:
        power.quick_shutdown()
        rsp = "server shutting down"
    # Super Admin tools
    elif msg == f'{summon}stop all' and settings["super_admin"] in roles:
        rsp = stop_all()
    # other stuff
    elif msg == f'{summon}ip':
        rsp = ips
    elif msg == f'{summon}live':
        server_live = ''
        for server in server_list:
            server_live += server.live() + '\n'
        rsp = server_live
    else:
        rsp = "unknown command"
    
    # make msg hangler 
    for server in server_list:
        server_rsp = server.std_commands(msg, summon, roles)
        if server_rsp:
            rsp = server_rsp

    await message.channel.send(rsp)


@client.event
async def on_member_update(prev, cur):
    pass
    # if cur.activities:
    #     curr_activity_names = [a.name for a in cur.activities]
    #     prev_activity_names = [a.name for a in prev.activities]
    #     if "League of Legends" in curr_activity_names and "League of Legends" not in prev_activity_names:
    #         judge_msg = f"{cur.mention} is playing League of Legends. Everyone be aware of this and judge them accordingly."
    #         send_message(bot_channels, judge_msg)

client.run(settings['private_token'])
