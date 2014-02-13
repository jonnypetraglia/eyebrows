import os
if os.name == 'nt':
    try:
        import win32api
        import win32con
    except ImportError:
        print("Install pywin32 if you want to")


## Formats a string of bytes
def formatBytes(inputInt):
    suffixes = ["", "K", "M", "G", "T"]
    i = 0
    while inputInt > 2000:
        inputInt /= 1024.0
        i += 1
    return "{0:.2f}".format(inputInt) + " " + suffixes[i] + "B"


def listdir(path, skiphidden):
    for f in os.listdir(path):
       if (not skiphidden) or (not is_hidden(os.path.join(path, f))):
           yield [f, os.path.isdir(os.path.join(path, f))]

def listdir_files(path, skiphidden):
    for f in os.listdir(path):
        if os.path.isfile(os.path.join(path, f)):
            if (not skiphidden) or (not is_hidden(os.path.join(path, f))):
                yield f


def listdir_dirs(path, skiphidden):
    for f in os.listdir(path):
        if os.path.isdir(os.path.join(path, f)):
            if (not skiphidden) or (not is_hidden(os.path.join(path, f))):
                yield f


#http://stackoverflow.com/questions/7099290/how-to-ignore-hidden-files-using-os-listdir-python
def is_hidden(p):
    if os.name == 'nt':
        attribute = win32api.GetFileAttributes(p)
        return attribute & (win32con.FILE_ATTRIBUTE_HIDDEN | win32con.FILE_ATTRIBUTE_SYSTEM)
    else:
        return os.path.basename(p).startswith('.')