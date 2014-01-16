# General socket/connection stuff
from http.server import HTTPServer
from http.server import SimpleHTTPRequestHandler
import urllib.parse
# SSL
from socketserver import BaseServer
import socket
import ssl
# Used for zip file generation
from zipstream import zipstream
# Misc
import os
from mako.template import Template
# Project files
from icontypes import fileIcons
from config import *


# Temp variables that are automatically set. DO NOT TOUCH
numBase = len(os.path.normpath(baseFolder).split(os.sep)) - 1
imgList = []
maintemplate = Template(filename='main.html')


### Main class that handles everything ###
class MyHandler(SimpleHTTPRequestHandler):
    def __init__(self, req, client_addr, server):
        SimpleHTTPRequestHandler.__init__(self, req, client_addr, server)

    ## Handle Get requests
    def do_GET(self):
        theArg = urllib.parse.unquote(self.path.split("?")[0])[1:]
        parameters = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        pathVar = os.path.join(baseFolder, theArg)
        # paths that start with /~ refer to the directory
        if theArg.startswith("~"):
            return self.getResource(theArg[2:])
        # Check for existence
        if not os.path.exists(pathVar):
            return self.notFound(theArg)
        # Handle the file or folder
        if os.path.isdir(pathVar):
            self.doFolder(theArg)
        if os.path.isfile(pathVar):
            self.downloadFile(theArg, parameters)

    ## Serve a resource that lives in the same folder as Eyebrows, such as CSS or JS
    def getResource(self, relPath):
        print("Resourcing: " + relPath)
        f = open(os.path.normpath(relPath), 'rb')
        self.send_response(200)
        self.send_header('Content-type', 'text/html;charset=utf-8')
        dat = f.read()
        self.send_header("Content-length", len(dat))
        if protocol == "HTTP/1.1":
            self.send_header('Connection', 'Close')
        self.end_headers()
        self.wfile.write(dat)
        self.wfile.flush()
        f.close()

    ## Download or view a file when requested from a GET
    def downloadFile(self, relPath, parameters):
        print("Downloading: " + relPath)
        if "i" in parameters and parameters["i"]:
            SimpleHTTPRequestHandler.do_GET(self)
            return

        derp, ext = os.path.splitext(relPath)
        ext = ext[1:].lower()
        f = open(os.path.join(baseFolder, relPath), 'rb')
        self.send_response(200)
        if ext == "html" or ext == "htm":
            self.send_header('Content-type', 'text/html;charset=utf-8')
        elif ext in fileIcons and (fileIcons[ext] == "file-text-o" or fileIcons[ext] == "code"):
            self.send_header('Content-type', 'text/plain;charset=utf-8')
        else:
            self.send_header('Content-type', 'application/octet-stream')
        dat = f.read()
        self.send_header("Content-length", len(dat))
        if protocol == "HTTP/1.1":
            self.send_header('Connection', 'Close')
        self.end_headers()
        self.wfile.write(dat)
        self.wfile.flush()
        f.close()

    ## Display a folder
    def doFolder(self, subfolder):
        global imgList
        folder = os.path.join(baseFolder, subfolder)
        if os.path.islink(folder):
            print("Found a symlink")
            folder = os.path.realpath(folder)

        link_dest = os.path.dirname(subfolder) if subfolder else ""
        page_title = os.path.basename(subfolder)
        nav_folders = os.path.normpath(os.path.join(baseFolder, subfolder)).split(os.sep)[numBase + 1:]

        folderList = [f for f in os.listdir(folder) if os.path.isdir(os.path.join(folder, f))]
        fileList = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]

        r = maintemplate.render(subfolder=subfolder,
                                link_dest=link_dest,
                                page_title=page_title,
                                nav_folders=nav_folders,
                                folderList=folderList,
                                fileList=fileList,
                                imgList=imgList,
                                hideBarsDelay=hideBarsDelay,
                                fileIcons=fileIcons,
                                baseFolder=baseFolder)
        print(r)

        self.send_response(200)
        self.send_header("Content-type", "text/html;charset=utf-8")
        self.send_header("Content-length", len(r))
        self.end_headers()
        self.wfile.write(r.encode("utf-8"))
        self.wfile.flush()

        return

    ## Respond to POSTs; used for requesting zip files
    def do_POST(self):
        length = int(self.headers['Content-Length'])
        post_data = urllib.parse.parse_qs(self.rfile.read(length).decode('utf-8'))
        print("Posted: ")
        print(post_data)
        self.downloadZip(post_data['subfolder'][0] if 'subfolder' in post_data else "", post_data['items'])

    ## Download a zip file
    def downloadZip(self, subfolder, files):
        print("Downloading Zip in folder: " + subfolder)
        self.send_response(200)
        self.send_header('Content-type', 'application/zip')
        self.send_header('Content-Disposition', 'attachment; filename="%s"' % ((subfolder if subfolder != "" else "Home") + ".zip"))
        self.end_headers()
        with zipstream.ZipFile(mode='w', compression=zipstream.ZIP_DEFLATED) as z:
            for f in files:
                fullpath = os.path.join(baseFolder, subfolder, f)
                if os.path.isdir(fullpath):
                    self._packFolder(z, subfolder, f)
                else:
                    z.write(fullpath, f)
            with open('test.zip', 'wb') as f:
                for chunk in z:
                    if chunk:
                        self.wfile.write(chunk)
        self.wfile.flush()

    ## Packs a folder inside the ZIP; is recursive
    def _packFolder(self, z, subfolder, target):
        folder = os.path.join(baseFolder, subfolder, target)
        folderList = [f for f in os.listdir(folder) if os.path.isdir(os.path.join(folder, f))]
        fileList = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
        for f in fileList:
            fullpath = os.path.join(baseFolder, subfolder, target, f)
            fulltarget = os.path.join(target, f)
            z.write(fullpath, arcname=fulltarget)
        for f in folderList:
            self._packFolder(z, subfolder, os.path.join(target, f))

    ## 404
    def notFound(self, folder):
        r = "Nope"
        self.send_response(404)
        self.send_header("Content-type", "text/html;charset=utf-8")
        self.send_header("Content-length", len(r))
        self.end_headers()
        self.wfile.write(r.encode("utf-8"))
        self.wfile.flush()


### Basically a HTTPServer with SSL ###
class SecureHTTPServer(HTTPServer):
    def __init__(self, server_address, HandlerClass):
        BaseServer.__init__(self, server_address, HandlerClass)
        self.socket = ssl.SSLSocket(
            sock=socket.socket(self.address_family, self.socket_type),
            ssl_version=ssl.PROTOCOL_TLSv1,
            certfile='server.pem',
            server_side=True)
        self.server_bind()
        self.server_activate()


try:
    server_address = ('0.0.0.0', port)
    MyHandler.protocol_version = protocol
    if useSSL:
        httpd = SecureHTTPServer(server_address, MyHandler)
    else:
        httpd = HTTPServer(server_address, MyHandler)
    print ("Server Started")
    httpd.serve_forever()
except KeyboardInterrupt:
    print('Shutting down server')
    httpd.socket.close()