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
cp "$configFile" bot.config
sed -i "s/\(tokenBot=\).*/\1$tokenBot/" bot.config
sed -i "s/\(guildId=\).*/\1$guildId/" bot.config
sed -i "s/\(channelId=\).*/\1$channelId/" bot.config

sudo apt-get update
sudo apt-get install -y python3 python3-pip curl nodejs npm gcc g++ make

python3 -m venv myenv
source myenv/bin/activate

pip3 install -r requirements.txt

sudo npm install -g pm2

pm2 start "python3 main.py" --name "Amazon-watch-price-bot"
pm2 save

sudo pm2 startup
