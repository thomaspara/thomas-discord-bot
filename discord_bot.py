import discord
import secrets
from process_manager import server_manager 
from power_manager import power_manager
print("bot started")

def remove_prefix(text, prefix):
    return text[text.startswith(prefix) and len(prefix):]

client = discord.Client()
summon="/cock "
srv_num = 0 #todo implement this

power = power_manager()
mc_v_server = server_manager("mcv", secrets.vanilla_mc_path)
ter_v_server = server_manager("terv", secrets.vanilla_ter_path)

help_msg = f'''to use me say `{summon}` 
I will ignore you if you have the Bot Banned role
Commands:
`minecraft start` starts minecraft server
`minecraft stop` stops minecraft server
`minecraft send <server command>` sends <server command> to server, requires Minecraft Admin role
`minecraft live` says if the server is live

`terraria start` starts terraria server
`terraria stop` stops terraria server
`terraria send <server command>` sends <server command> to server, requires Minecraft Admin role
`terraria live` says if the server is live

`live` shows status of all servers
`ip` shows ip list
`help` shows this message'''

ips = f'''server list
`{secrets.vanilla_mc_ip}` minecraft
`{secrets.vanilla_ter_ip}` terraria
Ask Thomas for help if you can't connect
'''

@client.event
async def on_message(message):
    if message.channel.name != secrets.bot_channel : return
    if message.author == client.user: return
    if not message.content.startswith(summon) : return 
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
        cmd = remove_prefix(msg,f'{summon} minecraft send ')
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
        cmd = remove_prefix(msg,f'{summon} terraria send ')
        if ter_v_server.send(cmd):
            rsp = f"sent `{cmd}`"
        else:
            rsp = "server is offline"
    #power management
    elif msg == f'{summon}reboot' and "Super Admin" in roles:
        power.reboot()
        rsp = "server rebooting"
    #Super Admin tools
    elif msg == f'{summon}stop all' and "Super Admin" in roles:
        rsp = ""
        if ter_v_server.is_running():
            ter_v_server.send("exit")
            rsp += "stopping terraria\n"
        if mc_v_server.is_running():
            mc_v_server.send("stop")
            rsp += "stopping minecraft\n"
        if rsp == "":
            rsp = "nothing is running"
    #other stuff
    elif msg == f'{summon}ip':
        rsp = ips
    elif msg == f'{summon}live':
        rsp = ""
        if ter_v_server.is_running():
            rsp += "terraria is running\n"
        if mc_v_server.is_running():
            rsp += "minecraft is running\n"
        if rsp == "":
            rsp = "nothing is running"
    else:
        rsp = "unknown command"

    await message.channel.send(rsp)

client.run(secrets.private_token)