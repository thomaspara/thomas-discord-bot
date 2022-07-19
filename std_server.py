from process_manager import server_manager 

def remove_prefix(text, prefix):
    return text[text.startswith(prefix) and len(prefix):]

class std_manager:

    def __init__(self,name,screen_name,cmd,ip,stop_word):
        self.server = server_manager(screen_name, cmd)
        self.name = name
        self.help = f'''`{name} start` starts {name} server
`{name} stop` stops {name} server
`{name} send <server command>` sends <server command> to server, requires {name.capitalize()} Admin role
`{name} live` says if the server is live'''
        self.ip = f'`{ip}` {name}'
        self.stop_word = stop_word

    def std_commands(self, msg, summon):
        rsp = ""
        if msg == f'{summon}{self.name} start':
            if self.server.start():
                rsp = f"starting server, be sure to run `{summon}{self.name} stop` when you are done"
            else:
                rsp = "server is running"
        elif msg == f'{summon}{self.name} stop':
            if self.server.send(self.stop):
                rsp = f"stopping {self.name}"
            else:
                rsp = "server already offline"
        elif msg == f'{summon}{self.name} live':
            if self.server.is_running():
                rsp = "server is running"
            else:
                rsp = "server is offline"
        elif f'{summon}{self.name} send ' in msg and f"{self.name.capitalize()} Admin" in roles:
            cmd = remove_prefix(msg,f'{summon}{self.name} send ')
            if self.server.send(cmd):
                rsp = f"sent `{cmd}`"
            else:
                rsp = "server is offline"
        return rsp
    
    def stop(self):
        if self.server.send('self.stop_word'):
            rsp = f"stopping {self.name}"
        else:
            rsp = f"{self.name} server already offline"
        return rsp
    
    def live(self):
        if self.server.is_running():
            rsp = f"{self.name} is running"
        else:
            rsp = f"{self.name} is offline"
        return rsp