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

        print(self.buffer.hex())

    def addstr(self, s):
        s = s.encode("utf-8")
        fmt = "<L{}s".format(len(s) + 1)
        self.buffer += pack(fmt, len(s)+1, s)
        self.size += calcsize(fmt)
        print(f"{self.size} : {self.buffer}")

    def addBytes(self, s, b): 
        fmt = "<L{}s".format(s)
        self.buffer += pack(fmt, s, str(b))
        self.size += calcsize(fmt)

    def addWstr(self, s):
        s = s.encode("utf-16_le")
        fmt = "<L{}s".format(len(s) + 2)
        self.buffer += pack(fmt, len(s)+2, s)
        self.size += calcsize(fmt)

def dcenum(demonID, *param):
    TaskID : str    = None
    demon  : Demon  = None
    packer = Packer()

    demon  = Demon( demonID )
    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to enumerate domain information using Active Directory Domain Services" )
    
    arg = packer.getbuffer() 

    demon.InlineExecute( TaskID, "go", "Domaininfo.o", "", False )

    return TaskID

RegisterCommand( dcenum, "", "dcenum", "enumerate domain information using Active Directory Domain Services", 0, "", "" )
