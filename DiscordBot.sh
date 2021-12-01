script_full_path=$(dirname "$(realpath "$0")")
cd $script_full_path
git fetch https://github.com/thomaspara/thomas-discord-bot.git
isRunning=$(screen -ls | grep discord_bot)
if [ -z "$isRunning" ]
then
	screen -mdS discord_bot start.sh
fi
