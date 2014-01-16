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
import time

# Project files
from icontypes import fileIcons


# Configuration variables
baseFolder = os.path.expanduser("~")
port = 8080
hideBarsDelay = 0
protocol = "HTTP/1.0"
useSSL = True


# Temp variables that are automatically set. DO NOT TOUCH
numBase = len(os.path.normpath(baseFolder).split(os.sep)) - 1
imgList = []



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

        folderList = [f for f in os.listdir(folder) if os.path.isdir(os.path.join(folder, f))]
        fileList = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
        r = []
        r.append('<html xmlns="http://www.w3.org/1999/xhtml" lang="en-US">')
        r.append('<head>')
        r.append('<link rel="icon" type="image/x-icon" href="/~/img/favicon.ico" />')
        r.append('<link href="//netdna.bootstrapcdn.com/bootstrap/3.0.3/css/bootstrap.min.css" rel="stylesheet">')
        r.append('<link href="//netdna.bootstrapcdn.com/font-awesome/4.0.3/css/font-awesome.css" rel="stylesheet">')
        r.append('<link href="/~/css/swipebox.css" rel="stylesheet">')
        r.append('<link href="/~/css/eyebrow.css" rel="stylesheet">')
        if os.path.basename(subfolder) != "":
            r.append('<title>' + os.path.basename(subfolder) + ' - Eyebrows</title>')
        else:
            r.append('<title>Eyebrows</title>')
        r.append('</head>')
        r.append('<body>')
        r.append('<form role="form" method="post" action="/">')
        r.append('<input type="hidden" name="subfolder" value="' + subfolder + '"></input>')
        r.append('<header class="container"><h1 class="col-sm-12" id="content"><img src="/~/img/logo-long.png" /></h1></header>')

        link = "/" + os.path.dirname(subfolder)
        if subfolder == "":
            link = "/"
        r.append('<nav class="affix" data-spy="affix" id="nav" data-offset-top="45" role="navigation">')
        r.append('<ol class="breadcrumb container">')
        r.append('<a class="btn btn-default" href="' + link + '" title="Up a Level"><i class="fa fa-level-up fa-flip-horizontal"></i></a>')
        r.append('<li><a href="/">Home</a></li>')
        folders = os.path.normpath(folder).split(os.sep)[numBase + 1:]
        link = []
        for f in folders:
            link.append(f)
            r.append('<li><a href="/' + '/'.join(link) + '">' + f + '</a></li>')
        r.append('<a class="btn btn-default pull-right" title="Upload"><i class="fa fa-upload"></i></a>')
        r.append('<button class="btn btn-default pull-right" title="Download"><i class="fa fa-download"></i><span id="dl-button"></span></button>')
        r.append('</ol></nav>')

        r.append('<div class="container">')
        r.append('<div class="col-sm-12">')
        r.append('<table id="file-list" class="table table-hover">')

        r.append("<tr><th><input type='checkbox' id='select-all'></th><th></th><th>Name</th><th>Size</th><th>Date</th></tr>")
        for f in folderList:
            r.append(self.getFolder(subfolder, f))

        for f in fileList:
            r.append(self.getFile(folder, subfolder, f))
        r.append('</table>')

        r.append('</div>')
        r.append('</div>')
        r.append('</form>')
        r.append('<script src="//code.jquery.com/jquery-1.10.2.min.js"></script>')
        r.append('<script src="//netdna.bootstrapcdn.com/bootstrap/3.0.3/js/bootstrap.min.js"></script>')
        r.append('<script src="/~/js/jquery.swipebox.min.js"></script>')
        r.append('<script type="text/javascript">')
        r.append('window.imageArray = [')
        r.append("\n{href:'/" + subfolder + "/" + imgList[0] + "', title:'" + imgList[0] + "'}")
        for i in imgList[1:]:
            r.append(",\n{href:'/" + subfolder + "/" + i.replace("'", "&#39;") + "', title:'" + i.replace("'", "&#39;") + "'}")
        r.append('];')

        r.append('hideBarsDelay = ' + str(hideBarsDelay) + ';')
        r.append('</script>')
        r.append('<script src="/~/js/eyebrows.js"></script>')
        r.append('</body>')
        r.append('</html>')
        r = '\n'.join(r)
        self.send_response(200)
        self.send_header("Content-type", "text/html;charset=utf-8")
        self.send_header("Content-length", len(r))
        self.end_headers()
        self.wfile.write(r.encode("utf-8"))
        self.wfile.flush()

    ## Returns a string of HTML for a file entry
    def getFile(self, folder, subfolder, name):
        derp, ext = os.path.splitext(name)
        ext = ext[1:].lower()
        if ext in fileIcons and fileIcons[ext] == "picture-o":
            imgList.append(name)

        link = "/".join([subfolder, name])
        if subfolder == "":
            link = name
        urllib.parse.quote(link)
        return "<tr><td><input type='checkbox' class='chk' name='items' value='" + name.replace("'", "&#39;") + "'></td>" + \
               "<td><i class='fa fa-" + (fileIcons[ext] if ext in fileIcons else "file-o") + "'></i></td>" + \
               "<td><a href='" + link + "'" + \
               (" class='img-file'" if ext in fileIcons else "") + ">" + name.replace("'", "&#39;") + "</a></td>" + \
               "<td><small>" + formatBytes(os.path.getsize(os.path.join(folder, name))) + "</small></td>" + \
               "<td><small>" + time.strftime('%b %d, %Y %I:%M%p', time.localtime(os.path.getmtime(os.path.join(folder, name)))) + "</small></td></tr>"

    ## Returns a string of HTML for a folder entry
    def getFolder(self, subfolder, name):
        link = "/".join([subfolder, name])
        if subfolder == "":
            link = name
        return "<tr><td><input type='checkbox' class='chk' name='items' value='" + name.replace("'", "&#39;") + "'></td><td><i class='fa fa-folder'></i></td>" + \
               "<td><a href='/" + link + "'>" + name + "</a></td><td></td><td></td></tr>"

    ## 404
    def notFound(self, folder):
        r = "Nope"
        self.send_response(404)
        self.send_header("Content-type", "text/html;charset=utf-8")
        self.send_header("Content-length", len(r))
        self.end_headers()
        self.wfile.write(r.encode("utf-8"))
        self.wfile.flush()

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

    ## Not used, currently; kept around because I'm not confident in downloadZip
    def downloadZip2(self, subfolder, files):
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
                    f.write(chunk)
        with open('test.zip', 'rb') as fi:
            self.wfile.write(fi.read())
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


## Formats a string of bytes
def formatBytes(inputInt):
    suffixes = ["", "K", "M", "G", "T"]
    i = 0
    while inputInt > 2000:
        inputInt /= 1024.0
        i += 1
    return "{0:.2f}".format(inputInt) + " " + suffixes[i] + "B"

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