from havoc import Demon, RegisterCommand
from struct import pack, calcsize

def dcenum(demonID, *param):
    TaskID : str    = None
    demon  : Demon  = None

    demon  = Demon( demonID )
    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to enumerate domain information using Active Directory Domain Services" )
    
    demon.InlineExecute( TaskID, "go", "Domaininfo.o", "", False )

    return TaskID

RegisterCommand( dcenum, "", "dcenum", "enumerate domain information using Active Directory Domain Services", 0, "", "" )
