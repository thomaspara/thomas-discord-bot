import discord
import secrets
from std_server import std_manager
from power_manager import power_manager
from discord.ext import commands, tasks
import time
import schedule
import threading
import asyncio

intents = discord.Intents.default()
intents.presences = True
intents.members = True
print(intents)
print("bot started")


def remove_prefix(text, prefix):
    return text[text.startswith(prefix) and len(prefix):]


client = discord.Client(intents=intents)
summon = "%cock "
srv_num = 0  # todo implement this
bot_channels = []

power = power_manager()
# make servers
server_list = [
    std_manager("minecraft", "mcv", secrets.vanilla_mc_path,secrets.vanilla_mc_ip, "stop"),
    std_manager("terraria", "terv", secrets.vanilla_ter_path,secrets.vanilla_ter_ip, "exit"),
    std_manager("rlcraft", "rlc", secrets.rlc_path,secrets.rlc_ip, "stop")
]

# make help message
server_instr = ''
for server in server_list:
    server_instr += server.help + '\n'

help_msg = f'''to use me say `{summon.strip()}` 
I will ignore you outside of {secrets.bot_channel} or if you have the Bot Banned role
Commands:
{server_instr}
`live` shows status of all servers
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
            if channel.name in secrets.bot_channel:
                bot_channels.append(channel)
    print(bot_channels)
    scheduled_jobs()
    run_scheduled_tasks.start()
    send_message(bot_channels, "bot online")
    judge_msg = ''


@client.event
async def on_message(message):
    if message.channel.name not in secrets.bot_channel:
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
    # make msg hangler
    for server in server_list:
        server_rsp = server.std_commands(msg, summon)
        if server_rsp:
            rsp = server_rsp
    # power management
    if msg == f'{summon}reboot' and "Super Admin" in roles:
        power.reboot()
        rsp = "server rebooting"
    elif msg == f'{summon}shutdown' and "Super Admin" in roles:
        power.quick_shutdown()
        rsp = "server shutting down"
    # Super Admin tools
    elif msg == f'{summon}stop all' and "Super Admin" in roles:
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

client.run(secrets.private_token)
