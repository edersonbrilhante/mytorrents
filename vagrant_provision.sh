#!/bin/bash

apt-get update
apt-get install git -y
apt-get install vim -y
apt-get install python3-pip -y
apt-get install python3-libtorrent -y

# openssl s_client -connect seriestorrent.tv:443 -servername seriestorrent.tv
mkdir /vagrant/series
