#!/bin/bash

set -e

if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <tokenBot>"
    exit 1
fi

tokenBot="$1"
configFile="bot.config.example"

cd "$(dirname "$0")"
cp "$configFile" bot.config
sed -i "s/\(tokenBot=\).*/\1$tokenBot/" bot.config

sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv curl nodejs npm gcc g++ make gnupg

# Mongo
curl -fsSL https://www.mongodb.org/static/pgp/server-8.0.asc | \
   sudo gpg -o /usr/share/keyrings/mongodb-server-8.0.gpg \
   --dearmor
echo "deb [ arch=amd64,arm64 signed-by=/usr/share/keyrings/mongodb-server-8.0.gpg ] https://repo.mongodb.org/apt/ubuntu noble/mongodb-org/8.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-8.0.list
sudo apt-get update
sudo apt-get install -y mongodb-org
sudo systemctl start mongod
sudo systemctl enable mongod

python3 -m venv myenv
source myenv/bin/activate
pip3 install -r requirements.txt

sudo npm install -g pm2
pm2 start "python3 main.py" --name "Amazon-watch-price-bot"
pm2 save
sudo pm2 startup
