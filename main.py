from http.server import HTTPServer
from http.server import SimpleHTTPRequestHandler

import time
import urllib.parse
import os
from os.path import expanduser

baseFolder = expanduser("~")
port = 8081


numBase = len(os.path.normpath(baseFolder).split(os.sep)) - 1


class MyHandler(SimpleHTTPRequestHandler):
    def __init__(self, req, client_addr, server):
        SimpleHTTPRequestHandler.__init__(self, req, client_addr, server)

    def do_GET(self):
        theArg = urllib.parse.unquote(self.path[1:])
        pathVar = os.path.join(baseFolder, theArg)
        print("Getting: " + self.path + "  " + pathVar + "  " + os.path.join(baseFolder, self.path))
        if not os.path.exists(pathVar):
            return self.notFound(self.path)
        if os.path.isdir(pathVar):
            self.doFolder(theArg)
        if os.path.isfile(pathVar):
            self.downloadFile(theArg)

    def downloadFile(self, relPath):
        print("Downloading: " + relPath)
        derp, ext = os.path.splitext(relPath)
        ext = ext[1:].lower()
        f = open(os.path.join(baseFolder, relPath), 'rb')
        self.send_response(200)
        if ext == "html" or ext == "htm":
            self.send_header('Content-type', 'text/html;charset=utf-8')
        elif ext in fileIcons and (fileIcons[ext]=="file-text-o" or fileIcons[ext]=="code"):
            self.send_header('Content-type', 'text/plain;charset=utf-8')
        else:
            self.send_header('Content-type', 'application/octet-stream')
        dat = f.read()
        self.send_header("Content-length", len(dat))
        self.end_headers()
        self.wfile.write(dat)
        self.wfile.flush()
        f.close()

    def doFolder(self, subfolder):
        folder = os.path.join(baseFolder, subfolder)
        print("Loading subfolder: " + subfolder)
        print("Loading folder: " + folder)


        folderList = [ f for f in os.listdir(folder) if os.path.isdir(os.path.join(folder,f)) ]
        fileList = [ f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder,f)) ]
        print(fileList)
        r = []
        r.append('<html xmlns="http://www.w3.org/1999/xhtml" lang="en-US">')
        r.append('<head>')
        r.append('<link href="//netdna.bootstrapcdn.com/bootstrap/3.0.3/css/bootstrap.min.css" rel="stylesheet">')
        r.append('<link href="//netdna.bootstrapcdn.com/font-awesome/4.0.3/css/font-awesome.css" rel="stylesheet">')
        if os.path.basename(subfolder)!="":
            r.append('<title>' + os.path.basename(subfolder) + ' - Eyebrows</title>')
        else:
            r.append('<title>Eyebrows</title>')
        r.append('</head>')
        r.append('<body>')


        r.append('<div class="container">')
        r.append('<div class="col-sm-12">')
        r.append('<h1>Eyebrows</h1>')
        link = "/" + os.path.dirname(subfolder)
        if subfolder == "":
            link = "/"
        r.append('<ol class="breadcrumb">')
        r.append('<a class="btn btn-default" href="' + link + '"><i class="fa fa-level-up fa-flip-horizontal"></i></a>')

        folders = os.path.normpath(folder).split(os.sep)[numBase+1:]
        r.append('<li><a href="/">Home</a></li>')
        link = []
        for f in folders:
            link.append(f)
            r.append('<li><a href="/' + '/'.join(link) + '">' + f + '</a></li>')
        r.append('</ol>')

        r.append('<table class="table table-hover">')
        r.append("<tr><th></th><th></th><th>Name</th><th>Size</th><th>Date</th></tr>")
        for f in folderList:
            r.append(self.getFolder(subfolder, f))

        for f in fileList:
            r.append(self.getFile(folder, subfolder, f))
        r.append('</table>')

        r.append('</div>')
        r.append('</div>')
        r.append('<script type="text/javascript" src="js/jquery.flexslider-min.js">')
        r.append('</body>')
        r.append('</html>')
        r = '\n'.join(r)
        self.send_response(200)
        self.send_header("Content-type", "text/html;charset=utf-8")
        self.send_header("Content-length", len(r))
        self.end_headers()
        self.wfile.write(r.encode("utf-8"))
        self.wfile.flush()

    def getFile(self, folder, subfolder, name):
        derp, ext = os.path.splitext(name)
        ext = ext[1:].lower()
        link = "/".join([subfolder, name])
        if subfolder == "":
            link = name
        return "<tr><td></td>" + \
               "<td><i class='fa fa-" + (fileIcons[ext] if ext in fileIcons else "file-o") + "'></i></td>" + \
               "<td><a href='" + link + "'>" + name + "</a></td>" + \
               "<td><small>" + formatBytes(os.path.getsize(os.path.join(folder, name))) + "</small></td>" + \
               "<td><small>" + time.strftime('%b %d, %Y %I:%M%p', time.localtime(os.path.getmtime(os.path.join(folder, name)))) + "</small></td></tr>"

    def getFolder(self, subfolder, name):
        print("Getting folder: " + subfolder + "  " + name)
        link = "/".join([subfolder, name])
        if subfolder == "":
            link = name
        return "<tr><td></td><td><i class='fa fa-folder'></i></td><td><a href='/" + link + "'>" + name + "</a></td><td></td><td></td></tr>"

    def notFound(self, folder):
        r = "Nope"
        self.send_response(404)
        self.send_header("Content-type", "text/html;charset=utf-8")
        self.send_header("Content-length", len(r))
        self.end_headers()
        self.wfile.write(r.encode("utf-8"))
        self.wfile.flush()



def formatBytes(inputInt):
    suffixes = ["", "K", "M", "G", "T"]
    i = 0
    while inputInt > 2000:
        inputInt/=1024.0
        i+=1
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
Protocol = "HTTP/1.1"

server_address = ('localhost', port)

HandlerClass.protocol_version = Protocol


try:
    httpd = HTTPServer(server_address, MyHandler)
    print ("Server Started")
    httpd.serve_forever()
except KeyboardInterrupt:
    print('Shutting down server')
    httpd.socket.close()
