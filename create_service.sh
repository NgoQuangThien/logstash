#!/bin/bash

DIRECTORY='/tools/logstash'

tar -zxvf logstash-7.17.4-linux-x86_64.tar.gz

if [[ ! -d "$DIRECTORY" ]]; then
	sudo mkdir -p $DIRECTORY >>/dev/null 2>&1
fi

sudo rm -rf logstash-7.17.4/config
sudo mv -f logstash-7.17.4/				$DIRECTORY/core
sudo cp -r config						$DIRECTORY
sudo python3 render_config.py
sudo cp -r pipeline						$DIRECTORY

sudo /tools/logstash/core/bin/system-install /tools/logstash/config/startup.options

sudo systemctl daemon-reload
sudo systemctl enable logstash
sudo systemctl restart logstash
sudo systemctl status logstash
