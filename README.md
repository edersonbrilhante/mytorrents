# My Torrents

This project is a tool to facilitate the download of last available episode of my list of series.

Database of torrent used: https://seriestorrent.tv

### Requirements:
VirtualBox - https://www.virtualbox.org/wiki/Downloads
<br>
Vagrant - https://www.vagrantup.com/downloads.html

### Installing:
```bash
$> git clone https://github.com/edersonbrilhante/mytorrents
$> cd mytorrents
$> vagrant plugin install vagrant-omnibus
$> vagrant up
```


### Mode to use:
```bash
$> vagrant ssh
$> cd /vagrant
$> python3 bot.py
```
