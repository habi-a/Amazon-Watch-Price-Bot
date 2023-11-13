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
apt-get update
apt-get install -y python3
pip3 install -r requirements.txt
sed -i "s/\(tokenBot=\).*/\1$tokenBot/" $configFile
sed -i "s/\(guildId=\).*/\1$guildId/" $configFile
sed -i "s/\(channelId=\).*/\1$channelId/" $configFile
mv $configFile bot.config
chmod +x main.py
nohup ./main.py > bot.log &
