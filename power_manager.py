import os
import time
from multiprocessing import Process
from subprocess import run, PIPE

class power_manager:

    #implement when I have wake on lan
    # def __init__(self):
    #     self.screen_name = screen_name
    #     self.cmd = cmd
    #     self.exit_word = exit_word

    # def _shutdown_helper(self, timer):
    #     t = timer if timer > 0 else 0
    #     os.system(f"shutdown +{t+5}")
    #     time.sleep(t*60)
    #     self.send(self.exit_word)

    # def shutdown(self, timer):
    #     if timer == "stop": 
    #         os.system("shutdown -c")
    #     p = Process( target = self._shutdown_helper, args = (int(timer),) )
    #     p.start()
    #     return f"shutdown in {timer} min"

    def reboot(self):
        os.system("sudo shutdown -r +1")