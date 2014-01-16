## Formats a string of bytes
def formatBytes(inputInt):
    suffixes = ["", "K", "M", "G", "T"]
    i = 0
    while inputInt > 2000:
        inputInt /= 1024.0
        i += 1
    return "{0:.2f}".format(inputInt) + " " + suffixes[i] + "B"