import cherrypy
import app.model as model
import mpd
import os,sys
from genshi.template import TemplateLoader
import threading
import pafy
loader = TemplateLoader(
    os.path.join(os.path.dirname(__file__), 'templates'),
    auto_reload=True
)

def reconnect(f):
    def wrapper(self,*args,**kwargs):
        try:
            self.client.ping()
        except:
            self.client.connect(self.mhost,self.mport)
        f(self,*args,**kwargs)
        self.client.close()
        self.client.disconnect()
    return wrapper
    
class Root(object):

    def __init__(self,config):
        self.client=mpd.MPDClient(use_unicode=True)
        pafy.set_api_key(config['APIkey'])
        self.mhost=config['mpd host']
        self.mport=config['mpd port']
        self.client.connect(self.mhost,self.mport)
        self.client.clear()
        self.client.timeout=30
        self.client.consume(1)
        self.playlist=[]
        self.alt=None
        self.loading=False
        self.update()
        self.playlistUp=threading.Thread(target=self.playlistSub)
        self.playlistUp.daemon=True
        self.playlistUp.start()
        self.statusUp=threading.Thread(target=self.statusSub)
        self.statusUp.daemon=True
        self.statusUp.start()
        
    def update(self):
        status=self.client.status()
        self.state=status['state']
        try:
            self.volume=int(status['volume'])
        except KeyError:
            self.volume=None
            
    @cherrypy.expose
    def index(self):
        tmpl = loader.load('index.html')
        return tmpl.generate(volume=self.volume,state=self.state,playlist=self.playlist,autoplay=self.alt,loading=self.loading).render('html', doctype='html')

    @cherrypy.expose
    def panel(self,up=False,down=False,playpause=False,next=False):
        if up:
            self.volUp()
        if down:
            self.volDown()
        if playpause:
            self.play_pause()
        if next:
            self.skipTrack()
        raise cherrypy.HTTPRedirect('/')
        return self.index()

    @cherrypy.expose
    @reconnect
    def removeTrack(self,ind):
        ind=int(ind)
        if self.playlist[ind].file==self.client.playlistid()[ind]['file']:
            self.client.delete(ind)
    @cherrypy.expose
    def nextAuto(self):
        self.alt=self.playlist[0].getNext()
        
    @cherrypy.expose
    def usePanel(self,value):
        if value=="up":
            if self.volume!=None:
                self.volUp()
        elif value=="down":
            if self.volume!=None:
                self.volDown()
        elif value=="playpause":
            self.play_pause()
        elif value=="next":
            self.skipTrack()
        elif value=="beginning":
            self.gotoBeginning()
        
    @reconnect
    def volUp(self):
        #self.update()
        up=5
        if self.volume<=95:
            self.volume+=up
            self.client.setvol(self.volume)  
        
        
    @reconnect
    def volDown(self):
        #self.update()
        down=5
        if self.volume>=5:
            self.volume-=down
            self.client.setvol(self.volume)  


        
    @reconnect
    def play_pause(self):
        #self.update()
        if self.state=='stop':
            self.client.play()
        else:
            self.client.pause()
        
    @reconnect
    def skipTrack(self):
        try: 
            self.client.next()
        except:
            pass

    @reconnect
    def gotoBeginning(self):
        try: 
            self.client.seekcur(0)
        except:
            pass
        
    @cherrypy.expose
    def queryUrl(self, result=''):
        kind,yturl=result.split(',')
        loader=threading.Thread(target=self.queue, args=(yturl,kind,))
        loader.start()
#        self.queue(yturl,kind)
        raise cherrypy.HTTPRedirect('/')
        return self.index()

    @cherrypy.expose
    def query(self, youtubeQuery='',max=20):
        results=model.ytSearch(youtubeQuery,max)
        tmpl = loader.load('search.html')
        return tmpl.generate(query=youtubeQuery,results=results).render('html', doctype='html')

    def queue(self, yturl='',kind=''):        
        @reconnect                    
        def appendPlaylist(self,t):
            self.playlist.append(track)
            self.client.add(track.file)
            if self.client.status()['playlistlength']=='1':
                self.client.play()        
                
        if kind=="video":
            try: 
                self.loading=True
                track=model.Track(yturl)
                appendPlaylist(self,track)
            except Exception as e:
                print(e) 
            finally:
                self.loading=False
        if kind=="playlist":
            pl=pafy.get_playlist(yturl)
            for i in pl['items']:
                try:
                    self.loading=True
                    track=model.Track(1,i['pafy'])
                    appendPlaylist(self,track)
                except Exception as e:
                    print(e)
                finally:                
                    self.loading=False
    
    def playlistSub(self):
        watcher=mpd.MPDClient(use_unicode=True)
        watcher.connect(self.mhost,self.mport)
        while True:
            watcher.idle('playlist')
            mpdSide={i['file'] for i in watcher.playlistinfo()}
            self.playlist=[i for i in self.playlist if i.file in mpdSide]
            songsNr=len(watcher.playlist())
            if songsNr==1:
                try:
                    self.alt=self.playlist[0].getNext()
                except:
                    self.alt=self.playlist[0].getNext('mix')
            elif songsNr==0:
                 if self.alt and len(watcher.playlist())==0:
                     self.playlist.append(self.alt)
                     watcher.add(self.alt.file)
                     watcher.play()
            else:
                if self.alt:
                    self.alt.annihilate()
                self.alt=None
            watcher.clearerror()
            
    def statusSub(self):
        watcher=mpd.MPDClient(use_unicode=True)
        watcher.connect(self.mhost,self.mport)
        while True:
            event=watcher.idle('mixer','player')
            status=watcher.status()
            if 'player' in event:
                self.state=status['state']
            if 'mixer' in event:
                try:
                    self.volume=int(status['volume'])
                except KeyError:
                    self.volume=None         
                    
