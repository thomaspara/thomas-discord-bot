while [ -z "$(fping google.com | grep alive)" ]
do
    echo "waiting for internet ..."
    sleep 3
done
echo "Internet is now online"
python3 discord_bot.py
