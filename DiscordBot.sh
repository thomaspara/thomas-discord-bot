#!/bin/bash
while [ -z "$(fping google.com | grep alive)" ]
do
    echo "waiting for internet ..."
    sleep 3
done
echo "Internet is now online"
script_full_path=$(dirname "$(realpath "$0")")
cd $script_full_path
git checkout .
git fetch https://github.com/thomaspara/thomas-discord-bot.git
git pull
chmod +x ./start.sh
isRunning=$(screen -ls | grep discord_bot)
if [ -z "$isRunning" ]
then
	screen -mdS discord_bot ./start.sh
fi
