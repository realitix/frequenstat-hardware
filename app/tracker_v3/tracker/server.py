# -*-coding:utf-8 -*
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import logging
import json

# Handler
class frequenstatHttpHandler(BaseHTTPRequestHandler):
	
	def do_GET(self):
		self.send_response(200)
		
		options = {
			'/testServer': testServer,
			'/listFiles': listFiles,
			'/getFile': getFile,
			'/deleteFile': deleteFile
		}
		
		key = self.path
		if self.path.find("?") != -1:
			key = self.path[0:self.path.find("?")]
			
		options[key]()
		
		def testServer():
			self.send_header('Content-type','text/plain')
			self.end_headers()
			self.wfile.write("1")
			
		def listFiles():
			names = []
			for name in os.listdir(self.pathFolderWaitingSend) : 
				if os.path.isfile(name) and not 'gitignore' in name:
					names.append(name)

			self.send_header('Content-type','application/json')
			self.end_headers()
			self.wfile.write(json.dumps({'files': names}))
		
		def getFile():
			queryUrl = self.path[self.path.find("?")+1:]
			filename = queryUrl['filename']
			f = open(Server.pathFolderWaitingSend + filename) 
			self.send_response(200)
			self.send_header('Content-type', 'application/x-bzip')
			self.end_headers()
			self.wfile.write(f.read())
			f.close()
			
		def deleteFile:
			queryUrl = self.path[self.path.find("?")+1:]
			filename = queryUrl['filename']
			os.remove(Server.pathFolderWaitingSend + filename) 
			self.send_response(200)
			self.send_header('Content-type', 'text/plain')
			self.end_headers()
			self.wfile.write("1")

# Starter
class Server(object):
    """
     Classe gérant le serveur
    """
	
	pathFolderWaitingSend = None
	
    def __init__(self, port=None, pathFolderWaitingSend=None):
        self.log = logging.getLogger()
        
        if port == None or pathFolderWaitingSend == None:
            self.log.critical("Le port est mal renseigné")
            raise ValueError("Le port est mal renseigné")

        self.port = port
        self.__class__.pathFolderWaitingSend = pathFolderWaitingSend

    def start(self):
		try:
			server = HTTPServer(('', self.port), frequenstatHttpHandler)
			self.log.info("Serveur démarré au port %d", self.port)
			server.serve_forever()
		except Exception:
			self.log.critical("Le serveur a été stoppé")
			server.socket.close()