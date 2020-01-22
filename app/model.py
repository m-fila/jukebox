import pafy
import time

from xml.dom.minidom import parseString
import xml.dom.minidom
from urllib.request import urlopen

class Track(object):

    queuedTracks=set()
    manifest='manifest.googlevideo.com/api/manifest/dash/'

    def __init__(self,yturl,vid=None):
        if yturl==0:
            self.file=' '
            self.thumbnail=''
            self.author=' '
            self.title=' '
            self.time=' '
            self.next=0
            self.videoid=''
        else:
            if vid!=None:
                ytvid=vid
            else:
                ytvid=pafy.new(yturl)
            stream=ytvid.getbestaudio()
            self.file=stream.url
            if self.manifest in self.file:
                src=urlopen(self.file).read().decode('utf-8')
                el = xml.dom.minidom.parseString(src).documentElement
                rep=el.getElementsByTagName("Representation")
                bestAudio=max(rep ,key= lambda x: int(x.getAttribute("audioSamplingRate") if x.hasAttribute("audioSamplingRate") else 0))
                self.file=bestAudio.getElementsByTagName("BaseURL")[0].childNodes[0].data
            self.thumbnail=ytvid.thumb
            self.author=ytvid.author
            self.title=ytvid.title
            self.time=ytvid.duration
            try:
                self.next =ytvid.mix
            except IndexError:
                self.next=[self]
            self.videoid=ytvid.videoid
            self.queuedTracks.add(self.title)
        
    def getNext(self,mechanism='related'):
        if mechanism=='mix':
            if self.next==0:
                return self
            else:    
                for track in self.next:
                    if track.title not in self.queuedTracks:                
                        break
                return Track(1,track)
        elif mechanism=='related':
            related=pafy.call_gdata('search',
                                    {'relatedToVideoId':self.videoid,
                                     'part':
                                     'snippet',
                                     'type':'video'})['items']
            for track in related:
                if track['snippet']['title'] not in self.queuedTracks:
                    break
            return Track('https://www.youtube.com/watch?v='+track['id']['videoId'])
        else:
            return self
                    
    def annihilate(self):
        self.queuedTracks.remove(self.title)

def ytSearch(query,max=10):
    q= {'q':query,
        'part':'id',
        'maxResults':max,
        'type':'video,playlist'
        }
    results=pafy.call_gdata('search',q)['items']
    videosIds=[i['id']['videoId']  for i in results if i['id']['kind']=='youtube#video']
    playlistsIds=[i['id']['playlistId']  for i in results if i['id']['kind']=='youtube#playlist']
#    print(results[0])
    ids=','.join(videosIds)
    videos=pafy.call_gdata('videos',{'id':ids,'part':'id,snippet,contentDetails'})['items']
    ids=','.join(playlistsIds)
    playlists=pafy.call_gdata('playlists',{'id':ids,'part':'id,snippet,contentDetails'})['items']
    #print(playlists)
    browsed=[videos.pop(0) if i['id']['kind']=='youtube#video' else playlists.pop(0) for i in results]
    return [ProxyItem(i) for i in browsed]

def ytBrowse(query,max=10):
    q= {'q':query,
        'part':'id',
        'maxResults':max,
        'type':'video'
        }
    results=pafy.call_gdata('search',q)['items']
    return results

class ProxyItem(object):
    def __init__(self,ytq):
        self.kind=ytq['kind'][8:]
        self.thumbnail=ytq['snippet']['thumbnails']['default']['url']
        self.title=ytq['snippet']['title']
        self.author=ytq['snippet']['channelTitle']
        self.id=ytq['id']
        if self.kind=='video':
            self.url='https://www.youtube.com/watch?v='+self.id
            raw_duration=ytq['contentDetails']['duration']
            secs=pafy.playlist.parseISO8591(raw_duration)   
            duration = time.strftime('%H:%M:%S', time.gmtime(secs))
            self.time= str(duration)        
        elif self.kind=='playlist':
            self.url='https://www.youtube.com/playlist?list='+self.id
            self.count=ytq['contentDetails']['itemCount']
if __name__=="__main__":
    a=Track('https://www.youtube.com/watch?v=LBRqNhloSpg')
    print(a.file)