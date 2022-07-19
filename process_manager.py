import os
import time
from multiprocessing import Process
from subprocess import run, PIPE

class server_manager:

    def __init__(self,screen_name,cmd):
        self.screen_name = screen_name
        self.cmd = cmd
    
    def is_running(self):
        proc = run(f"screen -ls {self.screen_name}", shell = True, stdout=PIPE, text=True).stdout
        return "No Sockets found in" not in proc

    def start(self):
        if not self.is_running():
            os.system(f'screen -mdS {self.screen_name} "{self.cmd}"')
            return True
        else:
            return False

    def send(self, msg):
        if self.is_running():
            os.system(f'screen -S {self.screen_name} -X stuff "{msg}\n"')
            return True
        else:
            return False

if __name__ == "__main__": 
    server = server_manager("vanilla", "/home/thomas/Games/mc_v_server/vanilla_start.sh")
    server.start()
    time.sleep(20)
    server.send("say poop")
    time.sleep(1)
    server.send("--beg--")
    time.sleep(1)
    server.send("list")
    time.sleep(1)
    server.send("--end--")