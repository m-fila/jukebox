from app.controller import Root
import cherrypy
import os.path
import json
import sys

import socket
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def main(config):
    if config['local host']==True:
        host='127.0.0.1'
    elif config['default host']==True:
        host=get_ip()
    else:
        host= config['custom host']
    absPath=os.path.abspath(os.path.dirname(__file__))
    cherrypy.config.update({
        'server.ssl_module':'builtin' if config['ssl']==True else None,
        'server.ssl_certificate':config['cert'] if config['ssl']==True else None,
        'server.ssl_private_key':config['privkey'] if config['ssl']==True else None,  
        'server.socket_host': host,
        'server.socket_port': config['port'],
        'tools.encode.on': True, 'tools.encode.encoding': 'utf-8',
        'tools.decode.on': True,
        'tools.trailing_slash.on': True,
        'tools.staticdir.root': os.path.join(absPath,'app'),
    })
    cherrypy.quickstart(Root(config), '/', {
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': 'static'
        }
    })

if __name__ == '__main__':
    with open(sys.argv[1]) as f:
        config=json.load(f)
    main(config)