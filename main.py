from http.server import HTTPServer
from http.server import SimpleHTTPRequestHandler

import time
import urllib.parse
import os
import socket
import ssl
from os.path import expanduser
from socketserver import BaseServer

baseFolder = expanduser("~")
port = 8080
hideBarsDelay = 0


numBase = len(os.path.normpath(baseFolder).split(os.sep)) - 1
imgList = []
parameters = []


class SecureHTTPServer(HTTPServer):
    def __init__(self, server_address, HandlerClass):
        BaseServer.__init__(self, server_address, HandlerClass)
        self.socket = ssl.SSLSocket(
            sock=socket.socket(self.address_family,self.socket_type),
            ssl_version=ssl.PROTOCOL_TLSv1,
            certfile='server.pem',
            server_side=True)
        self.server_bind()
        self.server_activate()


class MyHandler(SimpleHTTPRequestHandler):
    def __init__(self, req, client_addr, server):
        SimpleHTTPRequestHandler.__init__(self, req, client_addr, server)

    def do_GET(self):
        print("Getting: " + self.path)

        theArg = urllib.parse.unquote(self.path.split("?")[0])[1:]

        if theArg.startswith("~"):
            return self.getResource(theArg[2:])

        parameters = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)

        pathVar = os.path.join(baseFolder, theArg)
        print("Getting: " + theArg + "  " + pathVar + "  " + os.path.join(baseFolder, theArg))
        if not os.path.exists(pathVar):
            return self.notFound(theArg)

        if os.path.isdir(pathVar):
            self.doFolder(theArg)
        if os.path.isfile(pathVar):
            self.downloadFile(theArg, parameters)

    def getResource(self, relPath):
        print("Resourcing: " + relPath)
        f = open(os.path.normpath(relPath), 'rb')
        self.send_response(200)
        self.send_header('Content-type', 'text/html;charset=utf-8')
        dat = f.read()
        self.send_header("Content-length", len(dat))
        #self.send_header('Connection', 'Close')
        self.end_headers()
        self.wfile.write(dat)
        self.wfile.flush()
        f.close()

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
        #self.send_header('Connection', 'Close')
        self.end_headers()
        self.wfile.write(dat)
        self.wfile.flush()
        f.close()

    def doFolder(self, subfolder):
        global imgList
        folder = os.path.join(baseFolder, subfolder)
        if os.path.islink(folder):
            print("Found a symlink")
            folder = os.path.realpath(folder)
        print("Loading subfolder: " + subfolder)
        print("Loading folder: " + folder + " " + str(os.path.islink(folder)))


        folderList = [ f for f in os.listdir(folder) if os.path.isdir(os.path.join(folder,f)) ]
        fileList = [ f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder,f)) ]
        print(fileList)
        r = []
        r.append('<html xmlns="http://www.w3.org/1999/xhtml" lang="en-US">')
        r.append('<head>')
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
        r.append('</ol></nav>')


        r.append('<div class="container">')
        r.append('<div class="col-sm-12">')

        r.append('<form role="form"><table id="file-list" class="table table-hover">')
        r.append("<tr><th><input type='checkbox' id='select-all'></th><th></th><th>Name</th><th>Size</th><th>Date</th></tr>")
        for f in folderList:
            r.append(self.getFolder(subfolder, f))

        for f in fileList:
            r.append(self.getFile(folder, subfolder, f))
        r.append('</table></form>')

        # Nice idea but does not work
        #imgList = [("\n{href:'/" + subfolder + "/" + i + "', title:'/" + subfolder + "/" + i + "'}") for i in imgList]
        print("imgList")
        print(imgList)

        r.append('</div>')
        r.append('</div>')
        r.append('<script src="//code.jquery.com/jquery-1.10.2.min.js"></script>')
        r.append('<script src="//netdna.bootstrapcdn.com/bootstrap/3.0.3/js/bootstrap.min.js"></script>')
        r.append('<script src="/~/js/jquery.swipebox.min.js"></script>')
        r.append('<script type="text/javascript">')
        r.append('window.imageArray = [')
        print("Yo so")
        r.append("\n{href:'/" + subfolder + "/" + imgList[0] + "', title:'" + imgList[0] + "'}")
        for i in imgList[1:]:
            r.append(",\n{href:'/" + subfolder + "/" + i.replace("'", "&#39;") + "', title:'" + i.replace("'", "&#39;") + "'}")
        # Again: nice idea, no worky.
        #r.append('window.imageArray = [' + ",".join(imgList) + "];")
        r.append('];')

        r.append('hideBarsDelay = ' + str(hideBarsDelay) + ';')
        r.append('</script>')
        r.append('<script src="/~/js/eyebrows.js"></script>')
        r.append('</body>')
        r.append('</html>')
        r = '\n'.join(r)
        print(r)
        self.send_response(200)
        self.send_header("Content-type", "text/html;charset=utf-8")
        self.send_header("Content-length", len(r))
        self.end_headers()
        self.wfile.write(r.encode("utf-8"))
        self.wfile.flush()
        print("Done")

    def getFile(self, folder, subfolder, name):
        derp, ext = os.path.splitext(name)
        ext = ext[1:].lower()
        if ext in fileIcons and fileIcons[ext] == "picture-o":
            imgList.append(name)

        link = "/".join([subfolder, name])
        if subfolder == "":
            link = name
        urllib.parse.quote(link)
        return "<tr><td><input type='checkbox' class='check' value='" + link + "'></td>" + \
               "<td><i class='fa fa-" + (fileIcons[ext] if ext in fileIcons else "file-o") + "'></i></td>" + \
               "<td><a href='" + link + "'" + \
               (" class='img-file'" if ext in fileIcons else "") + ">" + name.replace("'","&#39;") + "</a></td>" + \
               "<td><small>" + formatBytes(os.path.getsize(os.path.join(folder, name))) + "</small></td>" + \
               "<td><small>" + time.strftime('%b %d, %Y %I:%M%p', time.localtime(os.path.getmtime(os.path.join(folder, name)))) + "</small></td></tr>"

    def getFolder(self, subfolder, name):
        print("Getting folder: " + subfolder + "  " + name)
        link = "/".join([subfolder, name])
        if subfolder == "":
            link = name
        return "<tr><td><input type='checkbox'></td><td><i class='fa fa-folder'></i></td>" + \
               "<td><a href='/" + link + "'>" + name + "</a></td><td></td><td></td></tr>"

    def notFound(self, folder):
        r = "Nope"
        self.send_response(404)
        self.send_header("Content-type", "text/html;charset=utf-8")
        self.send_header("Content-length", len(r))
        self.end_headers()
        self.wfile.write(r.encode("utf-8"))
        self.wfile.flush()

    def clickImg(self, name):
        r = []


def formatBytes(inputInt):
    suffixes = ["", "K", "M", "G", "T"]
    i = 0
    while inputInt > 2000:
        inputInt /= 1024.0
        i += 1
    return "{0:.2f}".format(inputInt) + " " + suffixes[i] + "B"


fileIcons = {
    '7z': 'archive',
    'ace': 'archive',
    'bz2': 'archive',
    'cab': 'archive',
    'dd': 'archive',
    'dmg': 'archive',
    'gz': 'archive',
    'iso': 'archive',
    'lz': 'archive',
    'lzma': 'archive',
    'pea': 'archive',
    'rar': 'archive',
    's7z': 'archive',
    'sea': 'archive',
    'sfx': 'archive',
    'tar': 'archive',
    'tbz2': 'archive',
    'tgz': 'archive',
    'xz': 'archive',
    'z': 'archive',
    'zip': 'archive',
    'zipx': 'archive',
    'ahk': 'code',
    'asm': 'code',
    'asp': 'code',
    'bas': 'code',
    'bat': 'code',
    'bsh': 'code',
    'build': 'code',
    'c': 'code',
    'cgi': 'code',
    'cmd': 'code',
    'cpp': 'code',
    'cs': 'code',
    'css': 'code',
    'cxx': 'code',
    'd': 'code',
    'di': 'code',
    'f': 'code',
    'f2k': 'code',
    'f90': 'code',
    'f95': 'code',
    'for': 'code',
    'h': 'code',
    'hpp': 'code',
    'htm': 'code',
    'html': 'code',
    'java': 'code',
    'js': 'code',
    'lisp': 'code',
    'lsp': 'code',
    'lua': 'code',
    'pas': 'code',
    'php': 'code',
    'pl': 'code',
    'py': 'code',
    'pyw': 'code',
    'rb': 'code',
    's': 'code',
    's90': 'code',
    'scm': 'code',
    'sh': 'code',
    'sql': 'code',
    'ss': 'code',
    'tcl': 'code',
    'v': 'code',
    'vb': 'code',
    'vbs': 'code',
    'vh': 'code',
    'vhd': 'code',
    'xaml': 'code',
    'xhtml': 'code',
    'avi': 'file-text-o',
        'conf': 'file-text-o',
    'csv': 'file-text-o',
    'doc': 'file-text-o',
    'docx': 'file-text-o',
        'ini': 'file-text-o',
    'odt': 'file-text-o',
    'pdf': 'file-text-o',
    'rtf': 'file-text-o',
    'tex': 'file-text-o',
    'txt': 'file-text-o',
    'asf': 'film',
    'asx': 'film',
    'avi': 'film',
    'dv': 'film',
    'm4v': 'film',
    'mkv': 'film',
    'mov': 'film',
    'mp4': 'film',
    'mpe': 'film',
    'mpeg': 'film',
    'mpeg1': 'film',
    'mpeg4': 'film',
    'mpg': 'film',
    'mpg2': 'film',
    'webm': 'film',
    'wmv': 'film',
    'xvid': 'film',
    'xml': 'code',
    'aiff': 'music',
    'aac': 'music',
    'flac': 'music',
    'm4a': 'music',
    'm4p': 'music',
    'mp3': 'music',
    'ogg': 'music',
    'opus': 'music',
    'wav': 'music',
    'wma': 'music',
    'bmp': 'picture-o',
    'gif': 'picture-o',
    'jpeg': 'picture-o',
    'jpg': 'picture-o',
    'png': 'picture-o',
    'tif': 'picture-o',
    'tiff': 'picture-o'
    }


HandlerClass = MyHandler
Protocol = "HTTP/1.0"

server_address = ('0.0.0.0', port)

HandlerClass.protocol_version = Protocol


try:
    #httpd = HTTPServer(server_address, MyHandler)
    httpd = SecureHTTPServer(server_address, MyHandler)
    print ("Server Started")
    httpd.serve_forever()
except KeyboardInterrupt:
    print('Shutting down server')
    httpd.socket.close()
