#!/bin/bash

set -e

if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <tokenBot> <guildId> <channelId>"
    exit 1
fi

tokenBot="$1"
guildId="$2"
channelId="$3"
configFile="bot.config.example"

cd "$(dirname "$0")"
cp $configFile bot.config
sed -i "s/\(tokenBot=\).*/\1$tokenBot/" bot.config
sed -i "s/\(guildId=\).*/\1$guildId/" bot.config
sed -i "s/\(channelId=\).*/\1$channelId/" bot.config
chmod +x main.py
apt-get update
apt-get install -y python3 python3-pip curl nodejs gcc g++ make
pip3 install -r requirements.txt
npm install -g pm2
pm2 startup
pm2 start "/usr/bin/python3 /app/Amazon-Watch-Price-Bot/main.py" --name "Amazon-watch-price-bot"
pm2 save
