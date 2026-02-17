#!/bin/bash
set -euo pipefail

sudo apt-get --update install docker\* -y

cd ../web_server
sudo docker build . -t ordayna-backend
echo "database:3306" > database_address
cd ../config

printf "Run by running run_on_linux.sh in the project root folder"

