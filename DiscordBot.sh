script_full_path=$(dirname "$(realpath "$0")")
cmd=$"python $script_full_path/discord_bot.py"
isRunning=$(screen -ls | grep discord_bot)
if [ -z "$isRunning" ]
then
	screen -mdS discord_bot $cmd
fi
