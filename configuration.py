import json
import os.path

if __name__ == "__main__": 
    settings = {
        "private_token":"YourTokenHere",
        "bot_channels":["bot-commands", "otherChannels"],
        "max_servers":2,
        "super_admin":"Super Admin",
        "summon_word":"%summonWord"
    }
    server = {
        'server_type':'std',
        'name':"YourServerName",
        'screen_name':'srcname',
        'cmd':'cmd',
        'ip':'ip:port',
        'stop_word':'stop',
        'admin_role':'xxx Admin'
    }

    if os.path.exists('config.json'):
        f = open('config.json')
        config = json.load(f)
        f.close()
        num_servers = int(input("Number of servers to add: "))
        config_file = {
            'settings' : config["settings"],
            'servers' : config["servers"] + [server] * num_servers
        }
    else:
        num_servers = int(input("Number of servers: "))

        config_file = {
            'settings' : settings,
            'servers' : [server] * num_servers
        }

    with open("config.json", "w") as f:
        json.dump(config_file, f,indent=4)

  
