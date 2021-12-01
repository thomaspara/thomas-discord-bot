import discord
import secrets
from process_manager import server_manager 
print("bot started")

def remove_prefix(text, prefix):
    return text[text.startswith(prefix) and len(prefix):]

client = discord.Client()
summon="/cock"
srv_num = 0 #todo implement this

mc_v_server = server_manager("mcv", secrets.vanilla_mc_path)
ter_v_server = server_manager("terv", secrets.vanilla_ter_path)

help_msg = f'''to use me say `{summon}` 
Commands:
`minecraft start` starts minecraft server
`minecraft send <server command>` sends <server command> to server
`minecraft live` says if the server is live
`terraria start` starts terraria server
`terraria send <server command>` sends <server command> to server
`terraria live` says if the server is live
`ip` shows ip list
`help` shows this message'''

ips = f'''server list
`{secrets.vanilla_mc_ip}` minecraft
`{secrets.vanilla_ter_ip}` terraria
Ask Thomas for help if you can't connect
'''

@client.event
async def on_message(message):
    if message.author == client.user: return
    if not message.content.startswith(summon) : return 
    roles = [r.name for r in message.author.roles]
    msg = message.content
    msg = msg.lower()

    if summon == msg or f'{summon} help' == msg:
        rsp = help_msg
    #vanilla minecraft
    elif msg == f'{summon} minecraft start':
        if mc_v_server.start():
            rsp = "starting server"
        else:
            rsp = "server is running"
    elif msg == f'{summon} minecraft live':
        if mc_v_server.is_running():
            rsp = "server is running"
        else:
            rsp = "server is offline"
    elif f'{summon} minecraft send ' in msg and "Minecraft Admin" in roles:
        cmd = remove_prefix(msg,f'{summon} minecraft send ')
        if mc_v_server.send(cmd):
            rsp = f"sent `{cmd}`"
        else:
            rsp = "server is offline"
    #vanilla terraria
    elif msg == f'{summon} terraria start':
        if ter_v_server.start():
            rsp = "starting server"
        else:
            rsp = "server is running"
    elif msg == f'{summon} terraria live':
        if ter_v_server.is_running():
            rsp = "server is running"
        else:
            rsp = "server is offline"
    elif f'{summon} terraria send ' in msg and "Terraria Admin" in roles:
        cmd = remove_prefix(msg,f'{summon} terraria send ')
        if ter_v_server.send(cmd):
            rsp = f"sent `{cmd}`"
        else:
            rsp = "server is offline"
    #other stuff
    elif msg == f'{summon} ip':
        rsp = ips
    else:
        rsp = "unknown command"

    await message.channel.send(rsp)

client.run(secrets.private_token)