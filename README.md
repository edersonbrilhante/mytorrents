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

### Customing your list of series:
To customize for your list of series, you need to change series.json.
Property "link" is link of serie. And the property "last_download" has link of last download done(Used and filled, by the script, to control which series was seen).
