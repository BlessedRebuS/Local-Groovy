[![GitHub branches](https://badgen.net/github/branches/Naereen/Strapdown.js)](https://github.com/BlessedRebuS/Local-Groovy/tree/self_download)

# Local-Groovy (Streams Music)
A simple python bot built on discord-py that streams songs from youtube with [youtube-dl](https://youtube-dl.org) and plays it locally on your server

## Requirements:
Put your `TOKEN ID` and your `BOT ID` in the file **bot.py**

 ```bash
pip3 install -r requirements.txt
```

## Start and Enable at boot
```bash
cd Local-Groovy

sudo su

cp pythonbot.service /lib/systemd/system

systemctl daemon-reload

start pythonbot.service 

enable pythonbot.service
```
## To DO:

- Queues
