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
apt-get install -y python3 python3-pip curl supervisor
pip3 install -r requirements.txt
cp $configFile bot.config
sed -i "s/\(tokenBot=\).*/\1$tokenBot/" bot.config
sed -i "s/\(guildId=\).*/\1$guildId/" bot.config
sed -i "s/\(channelId=\).*/\1$channelId/" bot.config
chmod +x main.py
mkdir -p /var/log/supervisord/
supervisord -c supervisord.conf
