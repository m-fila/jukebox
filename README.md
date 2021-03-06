# Jukebox ![Alt text](app/static/subwoofer.png "jukebox")
python youtube player with web interface
## About
Tired of hanging on jack, drained by streaming bluetooth, infuriated by no playing in background? Stoppping audio and loud ads? Here's jukebox: grab some speakers/sound system, connect them to your computer/phone and run jukebox on it, control what you are listening to from minimalistic web interface. 

<p align="center">
  <img src="https://github.com/m-fila/jukebox/blob/master/docs/screen.png" alt='screenshot'>
</p>

## Getting started
Jukebox uses `youtube-dl` and `pafy` for communication with YouToube. The web interface is run with `cherrypy` and `genshi`. The playback is realized using music player daemon (`mpd`) and it's python client `python-mpd2.` The python dependencies are:
```
pip install cherrypy Genshi python-mpd2 youtube_dl pafy
```
Moreover you should have `mpd` built from source or from your repo (even the outdated Debian packages are fine):
```
sudo apt install mpd
or
sudo pacman -S mpd
or
sudo xbps-install -S mpd
or
...

```
Now you'll have to [generate YouTube-Data API key](https://developers.google.com/youtube/registering_an_application). At the time of writting google gives 10k free entries to each key every day (which is enough for this personal usage project). Once you have the key add in to the `config.json` file.
## Usage
On system connected to speakers or sound system run:
```
python __init.py__ config.json
```
to start jukebox. If successful a web interface should be availible at address specified in congifuration.

Due to live changes to YouTube remember to keep youtube_dl up to date:
```
pip install youtube_dl -U
```
### Configuration
config.json file:
```
{
    "port": 8080,                 port for web interface
    "local host": false,          web interface at localhost
    "default host": true,         web interface at primary host if "local host"==false
    "custom host": "127.0.0.1",   custom web interface host if "default host"==false
    "mpd host": "127.0.0.1",      custom mpd server host (default localhost)
    "mpd port": 6600,             custom mpd server port (default 6600)
    "ssl": false,                 enables ssl encryption for https connection
    "cert": "cert.pem" ,          path to ssl certificate
    "privkey": "privkey.pem",     path to ssl privkey
    "APIkey":" "                  your YouTube-Data API key goes here
}
```
SSL isn't supported yet!!

## Features
- [x] playback videos (audio) and playlists
- [x] browsing YouTube for videos and playlists
- [x] video queue
- [x] simple parsing YouTube dash manifests
- [x] http web interface
- [x] mobile friendly
- [x] control panel
- [x] autoplay next audio
- [ ] https web interface
- [ ] saving sessions
- [ ] spotify?
## Troubleshooting
* ```ERROR: xxxxxxxxxxx: Youtube says: Unable to extract video data```
means you have to update youtube_dl with `pip install youtube_dl -U`,

## License
Distributed under the GPL-3.0. See `LICENSE` for more information.
## Resources
* [cherrypy](https://cherrypy.org/) - framework
* [genshi](https://genshi.edgewall.org/) - templating
* [mini.css](https://minicss.org/) - css
* [fontawesome4](https://fontawesome.com/v4.7.0/icons/) - icons
* [icons8](https://icons8.com/icons/) - favicon
