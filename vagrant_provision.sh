#!/bin/bash

apt-get update
apt-get install git -y
apt-get install vim -y
apt-get install python3 -y
apt-get install python3-pip -y
apt-get install python3-dev -y
apt-get install python3-libtorrent -y
apt-get install python3-lxml -y

apt-get install python-lxml -y
apt-get install python-dev -y
apt-get install build-essential -y
apt-get install libssl-dev -y
apt-get install libffi-dev -y
apt-get install libxml2-dev -y
apt-get install libxslt1-dev -y
apt-get install zlib1g-dev -y
apt-get install python-pip -y

if [ ! -d /vagrant/series ]; then
    mkdir
fi

pip3 install -r /vagrant/requirements.txt
