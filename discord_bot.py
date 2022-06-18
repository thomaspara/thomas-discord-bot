import discord
import secrets
from process_manager import server_manager 
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
summon="%cock "
srv_num = 0 #todo implement this
bot_channels = []

power = power_manager()
mc_v_server = server_manager("mcv", secrets.vanilla_mc_path)
ter_v_server = server_manager("terv", secrets.vanilla_ter_path)
rlc_server = server_manager("rlc", secrets.rlc_path)

help_msg = f'''to use me say `{summon.strip()}` 
I will ignore you outside of {secrets.bot_channel} or if you have the Bot Banned role
Commands:
`minecraft start` starts minecraft server
`minecraft stop` stops minecraft server
`minecraft send <server command>` sends <server command> to server, requires Minecraft Admin role
`minecraft live` says if the server is live

`terraria start` starts terraria server
`terraria stop` stops terraria server
`terraria send <server command>` sends <server command> to server, requires Terraria Admin role
`terraria live` says if the server is live

`rlcraft start` starts rlcraft server
`rlcraft stop` stops rlcraft server
`rlcraft send <server command>` sends <server command> to server, requires RLCraft Admin role
`rlcraft live` says if the server is live

`live` shows status of all servers
`ip` shows ip list
`help` shows this message'''

ips = f'''server list
`{secrets.vanilla_mc_ip}` minecraft
`{secrets.vanilla_ter_ip}` terraria
`{secrets.rlc_ip}` rlcraft
Ask Thomas for help if you can't connect
'''

judge_msg = ''

async def send_message_helper(channel, msg):
    await channel.send(msg)

def send_message(channels, msg):
    for channel in channels:
        client.loop.create_task(send_message_helper(channel, msg))

def stop_all():
        rsp = ""
        if ter_v_server.is_running():
            ter_v_server.send("exit")
            rsp += "stopping terraria\n"
        if mc_v_server.is_running():
            mc_v_server.send("stop")
            rsp += "stopping minecraft\n"
        if rlc_server.is_running():
            rlc_server.send("stop")
            rsp += "stopping rlcraft\n"
        if rsp == "":
            rsp = "nothing is running"
        return rsp

def scheduled_jobs():
    schedule.every().day.at("06:00").do(send_message, channels=bot_channels, msg="server rebooting, stopping all running servers")
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

@client.event
async def on_message(message):
    if message.channel.name not in secrets.bot_channel : return
    if message.author == client.user: return
    if not message.content.startswith(summon.strip()) : return 
    roles = [r.name for r in message.author.roles]
    if "Bot Banned" in roles: return
    msg = message.content
    msg = msg.lower().strip()

    if summon.strip() == msg or f'{summon}help' == msg:
        rsp = help_msg
    #vanilla minecraft
    elif msg == f'{summon}minecraft start':
        if mc_v_server.start():
            rsp = f"starting server, be sure to run `{summon}minecraft stop` when you are done"
        else:
            rsp = "server is running"
    elif msg == f'{summon}minecraft stop':
        if mc_v_server.send('stop'):
            rsp = "stopping minecraft"
        else:
            rsp = "server already offline"
    elif msg == f'{summon}minecraft live':
        if mc_v_server.is_running():
            rsp = "server is running"
        else:
            rsp = "server is offline"
    elif f'{summon}minecraft send ' in msg and "Minecraft Admin" in roles:
        cmd = remove_prefix(msg,f'{summon}minecraft send ')
        if mc_v_server.send(cmd):
            rsp = f"sent `{cmd}`"
        else:
            rsp = "server is offline"
    #vanilla terraria
    elif msg == f'{summon}terraria start':
        if ter_v_server.start():
            rsp = f"starting server, be sure to run `{summon}terraria stop` when you are done"
        else:
            rsp = "server is running"
    elif msg == f'{summon}terraria stop':
        if ter_v_server.send('exit'):
            rsp = "stopping terraria"
        else:
            rsp = "server already offline"
    elif msg == f'{summon}terraria live':
        if ter_v_server.is_running():
            rsp = "server is running"
        else:
            rsp = "server is offline"
    elif f'{summon}terraria send ' in msg and "Terraria Admin" in roles:
        cmd = remove_prefix(msg,f'{summon}terraria send ')
        if ter_v_server.send(cmd):
            rsp = f"sent `{cmd}`"
        else:
            rsp = "server is offline"
    #rlcraft
    elif msg == f'{summon}rlcraft start':
        if rlc_server.start():
            rsp = f"starting server, be sure to run `{summon}rlcraft stop` when you are done"
        else:
            rsp = "server is running"
    elif msg == f'{summon}rlcraft stop':
        if rlc_server.send('stop'):
            rsp = "stopping rlcraft"
        else:
            rsp = "server already offline"
    elif msg == f'{summon}rlcraft live':
        if rlc_server.is_running():
            rsp = "server is running"
        else:
            rsp = "server is offline"
    elif f'{summon}rlcraft send ' in msg and "RLCraft Admin" in roles:
        cmd = remove_prefix(msg,f'{summon}rlcraft send ')
        if rlc_server.send(cmd):
            rsp = f"sent `{cmd}`"
        else:
            rsp = "server is offline"
    #power management
    elif msg == f'{summon}reboot' and "Super Admin" in roles:
        power.reboot()
        rsp = "server rebooting"
    elif msg == f'{summon}shutdown' and "Super Admin" in roles:
        power.quick_shutdown()
        rsp = "server shutting down"      
    #Super Admin tools
    elif msg == f'{summon}stop all' and "Super Admin" in roles:
        rsp = stop_all()
    #other stuff
    elif msg == f'{summon}ip':
        rsp = ips
    elif msg == f'{summon}live':
        rsp = ""
        if ter_v_server.is_running():
            rsp += "terraria is running\n"
        if mc_v_server.is_running():
            rsp += "minecraft is running\n"
        if rlc_server.is_running():
            rsp += "rlcraft is running\n"
        if rsp == "":
            rsp = "nothing is running"
    else:
        rsp = "unknown command"

    await message.channel.send(rsp)

@client.event
async def on_member_update(prev, cur):
    if cur.activities:
        activity_names = [a.name for a in cur.activities]
        if "League of Legends" in activity_names:
            new_msg = f"{cur.mention} is playing League of Legends. Everyone be aware of this and judge them accordingly."
            if new_msg != judge_msg:
                judge_msg = new_msg
                send_message(bot_channels, new_msg)

client.run(secrets.private_token)