from tkinter import *
from tkinter import ttk
from tkinter.filedialog import askdirectory
from eyebrows import *



def startServer():
    global server
    startServerBtn.configure(state='disabled')
    stopServerBtn.configure(state='enabled')
    server = Server()
    server.start()
    pass

def stopServer():
    global server
    stopServerBtn.configure(state='disabled')
    startServerBtn.configure(state='enabled')
    server.shutdown()
    server = None
    pass

def browseBaseFolder():
    tempvar = askdirectory(mustexist=True, initialdir=baseFolder)
    if tempvar:
        new_['baseFolder'].set(tempvar)
    pass

def closeWindow():
    if server:
        server.shutdown()
    root.quit()


# Apply button is pressed; do validations, save config to file, and reload server if necessary
def applyNow():
    global server
    needsRestart = config.useSSL != (new_['useSSL'].get()!='0') or config.port != int(new_['port'].get())
    # Do some validations
    config.baseFolder = new_['baseFolder'].get()
    config.port = int(new_['port'].get())
    config.useSSL = new_['useSSL'].get()!='0'
    config.protocol = new_['protocol'].get()
    config.hideBarsDelay = int(new_['hideBarsDelay'].get())
    config.useDots = new_['useDots'].get()!='0'
    config.sortFoldersFirst = new_['sortFoldersFirst'].get()!='0'
    config.uploadEnabled = new_['uploadEnable'].get()!='0'
    config.ignoreHidden = new_['ignoreHidden'].get()!='0'
    config.strictIgnoreHidden = new_['strictIgnoreHidden'].get()!='0'
    config.username = new_['username'].get()
    config.password = new_['password'].get()
    config.saveToFile
    setConfig()
    if needsRestart and server!=None:
        stopServer()
        startServer()

root = Tk()
root.title("Eyebrows")
root.protocol("WM_DELETE_WINDOW", closeWindow)

# Load the config
new_ = {}
for c in ['baseFolder', 'port', 'useSSL', 'protocol', 'hideBarsDelay', 'useDots', 'sortFoldersFirst', 'uploadEnable', 'ignoreHidden', 'strictIgnoreHidden', 'username', 'password']:
    new_[c] = StringVar()
new_['baseFolder'].set(config.baseFolder)
new_['port'].set(config.port)
new_['useSSL'].set(config.useSSL)
new_['protocol'].set(config.protocol)
new_['hideBarsDelay'].set(config.hideBarsDelay)
new_['useDots'].set(config.useDots)
new_['sortFoldersFirst'].set(config.sortFoldersFirst)
new_['uploadEnable'].set(config.uploadEnabled)
new_['ignoreHidden'].set(config.ignoreHidden)
new_['strictIgnoreHidden'].set(config.strictIgnoreHidden)
new_['username'].set(config.username)
new_['password'].set(config.password)


## Create the GUI
mainframe = ttk.Frame(root, padding="3 3 12 12")
mainframe.pack()
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

notebook = ttk.Notebook(mainframe)
notebook.grid(column=2, row=1, sticky=(W, E))

# Main tab
mainTab = ttk.Frame(notebook)
startServerBtn = ttk.Button(mainTab, text="Start Server", command=startServer)
stopServerBtn = ttk.Button(mainTab, text="Stop Server", command=stopServer)
stopServerBtn.configure(state='disabled')

startServerBtn.pack(padx=10, pady=10)
stopServerBtn.pack(padx=10, pady=10)
notebook.add(mainTab, text="Main")

# Config tab
configTab = ttk.Frame(notebook)

baseFolderLabel = ttk.Label(configTab, text="Base Folder")
baseFolderEntry = ttk.Entry(configTab, width=50, textvariable=new_['baseFolder'])
baseFolderBtn = ttk.Button(configTab, text="Browse", command=browseBaseFolder)

portLabel = ttk.Label(configTab, text="Port (requires restart)")
portSpinbox = Spinbox(configTab, from_=0, to=65535, width=8, textvariable=new_['port'])
useSSLCheckbutton = ttk.Checkbutton(configTab, text='SSL (requires restart)', variable=new_['useSSL'])
protocolLabel = ttk.Label(configTab, text="Protocol")
protocolOptionMenu = ttk.OptionMenu(configTab, new_['protocol'], None, 'HTTP/1.0', 'HTTP/1.1')

hideBarsDelayLabel = ttk.Label(configTab, text="Image Control Hide Delay (ms)")
hideBarsDelaySpinbox = Spinbox(configTab, from_=0, to=10000, width=8, textvariable=new_['hideBarsDelay'])
useDotsCheckbutton = ttk.Checkbutton(configTab, text='Use dots', variable=new_['useDots'])
sortFoldersFirstCheckbutton = ttk.Checkbutton(configTab, text='Sort folders first', variable=new_['sortFoldersFirst'])

uploadEnabledCheckbutton = ttk.Checkbutton(configTab, text='Upload Enabled', variable=new_['uploadEnable'])
ignoreHiddenCheckbutton = ttk.Checkbutton(configTab, text='Ignore Hidden Files', variable=new_['ignoreHidden'])
strictIgnoreHiddenCheckbutton = ttk.Checkbutton(configTab, text='Strict', variable=new_['strictIgnoreHidden'])

usernameLabel = ttk.Label(configTab, text='Username')
usernameEntry = ttk.Entry(configTab, width=15, textvariable=new_['username'])
passwordLabel = ttk.Label(configTab, text='Password')
passwordEntry = ttk.Entry(configTab, width=15, textvariable=new_['password'])


baseFolderLabel.grid(column=0, row=0, columnspan=10, sticky=(W))
baseFolderEntry.grid(column=0, row=1, columnspan=10, sticky=(W, E))
baseFolderBtn.grid(column=11, row=1, sticky=(W, E))
portLabel.grid(column=0, row=2, sticky=W)
portSpinbox.grid(column=0, row=3, sticky=W)
useSSLCheckbutton.grid(column=1, row=3, sticky=W)
protocolLabel.grid(column=2, row=2, sticky=W)
protocolOptionMenu.grid(column=2, row=3, sticky=W)
hideBarsDelayLabel.grid(column=0, row=4, sticky=W, columnspan=2)
hideBarsDelaySpinbox.grid(column=0, row=5, sticky=W, columnspan=2)
useDotsCheckbutton.grid(column=2, row=5, sticky=W)
sortFoldersFirstCheckbutton.grid(column=3, row=5, sticky=W)
uploadEnabledCheckbutton.grid(column=0, row=6, sticky=W)
ignoreHiddenCheckbutton.grid(column=2, row=6, sticky=W)
strictIgnoreHiddenCheckbutton.grid(column=3, row=6, sticky=W)
usernameLabel.grid(column=0, row=7, sticky=W)
passwordLabel.grid(column=1, row=7, sticky=W)
usernameEntry.grid(column=0, row=8, sticky=W)
passwordEntry.grid(column=1, row=8, sticky=W)
ttk.Button(configTab, text='Apply', command=applyNow).grid(column=11, row=10, sticky=E)


notebook.add(configTab, text="Config")

# Log tab
logTab = ttk.Frame(notebook)

# About tab
aboutTab = ttk.Frame(notebook)

root.mainloop()

