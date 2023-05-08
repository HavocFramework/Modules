from havoc import Demon, RegisterCommand, RegisterModule
import json
import re
import os

class SAPacker:
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

def arp( demonID, *param ):
    TaskID : str    = None
    demon  : Demon  = None

    demon  = Demon( demonID )
    TaskID = demon.ConsoleWrite(demon.CONSOLE_TASK, "Tasked demon to lists out ARP table")

    demon.InlineExecute( TaskID, "go", f"ObjectFiles/arp.{demon.ProcessArch}.o", b'', False )

    return TaskID

def driversigs( demonID, *param ):
    TaskID : str    = None
    demon  : Demon  = None

    demon  = Demon( demonID )
    TaskID = demon.ConsoleWrite(demon.CONSOLE_TASK, "Tasked demon to check drivers for known edr vendor names")

    demon.InlineExecute( TaskID, "go", f"ObjectFiles/driversigs.{demon.ProcessArch}.o", b'', False )

    return TaskID

def ipconfig( demonID, *param ):
    TaskID : str    = None
    demon  : Demon  = None

    demon  = Demon( demonID )
    TaskID = demon.ConsoleWrite(demon.CONSOLE_TASK, "Tasked demon to lists out adapters, system hostname and configured dns serve")

    demon.InlineExecute( TaskID, "go", f"ObjectFiles/ipconfig.{demon.ProcessArch}.o", b'', False )

    return TaskID

def ipconfig_with_callback( demonID, callback, *params ):
    demon  : Demon  = None
    demon  = Demon( demonID )

    return demon.InlineExecuteGetOutput( callback, "go", f"ObjectFiles/ipconfig.{demon.ProcessArch}.o", b'' )


def listdns( demonID, *param ):
    TaskID : str    = None
    demon  : Demon  = None

    demon  = Demon( demonID )
    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to lists dns cache entries" )

    demon.InlineExecute( TaskID, "go", f"ObjectFiles/listdns.{demon.ProcessArch}.o", b'', False )

    return TaskID

def locale( demonID, *param ):
    TaskID : str    = None
    demon  : Demon  = None

    demon  = Demon( demonID )
    TaskID = demon.ConsoleWrite(demon.CONSOLE_TASK, "Tasked demon to retrieve system locale information, date format, and country")

    demon.InlineExecute( TaskID, "go", f"ObjectFiles/locale.{demon.ProcessArch}.o", b'', False )

    return TaskID

def netstat( demonID, *param ):
    TaskID : str    = None
    demon  : Demon  = None

    demon  = Demon( demonID )
    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to get local ipv4 udp/tcp listening and connected ports" )

    demon.InlineExecute( TaskID, "go", f"ObjectFiles/netstat.{demon.ProcessArch}.o", b'', False )

    return TaskID

def resources( demonID, *param ):
    TaskID : str    = None
    demon  : Demon  = None

    demon  = Demon( demonID )
    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to list available memory and space on the primary disk drive" )

    demon.InlineExecute( TaskID, "go", f"ObjectFiles/resources.{demon.ProcessArch}.o", b'', False )

    return TaskID

def routeprint( demonID, *param ):
    TaskID : str    = None
    demon  : Demon  = None

    demon  = Demon( demonID )
    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to prints ipv4 routes on the machine" )

    demon.InlineExecute( TaskID, "go", f"ObjectFiles/routeprint.{demon.ProcessArch}.o", b'', False )

    return TaskID

def uptime( demonID, *param ):
    TaskID : str    = None
    demon  : Demon  = None

    demon  = Demon( demonID )
    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to lists system boot time" )

    demon.InlineExecute( TaskID, "go", f"ObjectFiles/uptime.{demon.ProcessArch}.o", b'', False )

    return TaskID

def uptime_with_callback( demonID, callback, *params ):
    demon  : Demon  = None
    demon  = Demon( demonID )

    return demon.InlineExecuteGetOutput( callback, "go", f"ObjectFiles/uptime.{demon.ProcessArch}.o", b'' )

def whoami( demonID, *param ):
    TaskID : str    = None
    demon  : Demon  = None

    demon  = Demon( demonID )
    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to get the info from whoami /all without starting cmd.exe" )

    demon.InlineExecute( TaskID, "go", f"ObjectFiles/whoami.{demon.ProcessArch}.o", b'', False )

    return TaskID

def whoami_with_callback( demonID, callback, *params ):
    demon  : Demon  = None
    demon  = Demon( demonID )

    return demon.InlineExecuteGetOutput( callback, "go", f"ObjectFiles/whoami.{demon.ProcessArch}.o", b'' )

def windowlist( demonID, *param ):
    TaskID : str    = None
    demon  : Demon  = None

    demon  = Demon( demonID )
    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to list windows visible on the users desktop" )

    demon.InlineExecute( TaskID, "go", f"ObjectFiles/windowlist.{demon.ProcessArch}.o", b'', False )

    return TaskID

def windowlist_with_callback( demonID, callback, *params ):
    demon  : Demon  = None
    demon  = Demon( demonID )

    return demon.InlineExecuteGetOutput( callback, "go", f"ObjectFiles/windowlist.{demon.ProcessArch}.o", b'' )

def reg_query_parse_params( demon, params ):
    packer = SAPacker()

    reghives = {
        'HKCR': 0,
        'HKCU': 1,
        'HKLM': 2,
        'HKU': 3
    }

    num_params = len(params)
    params_parsed = 0

    if num_params < 2:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Missing parameters" )
        return None

    if num_params > 4:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return None

    if params[ params_parsed ].upper() not in reghives:
        hostname = params[ params_parsed ]
        params_parsed += 1
    else:
        hostname = None

    if params[ params_parsed ].upper() not in reghives:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Provided registry hive value is invalid" )
        return None

    hive = reghives[ params[ params_parsed ].upper() ]
    params_parsed += 1

    if num_params < params_parsed + 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Missing parameters" )
        return None

    path = params[ params_parsed ]
    params_parsed += 1

    if num_params > params_parsed:
        key = params[ params_parsed ]
    else:
        key = None

    packer.addstr(hostname)
    packer.adduint32(hive)
    packer.addstr(path)
    packer.addstr(key)
    packer.addbool(False) # recursive

    return packer.getbuffer()

def reg_query( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    demon  = Demon( demonID )

    packed_params = reg_query_parse_params( demon, params )
    if packed_params is None:
        return False

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to query the windows registry" )

    demon.InlineExecute( TaskID, "go", f"ObjectFiles/reg_query.{demon.ProcessArch}.o", packed_params, False )

    return TaskID

def reg_query_with_callback( demonID, callback, *params ):
    demon  : Demon  = None
    demon  = Demon( demonID )

    packed_params = reg_query_parse_params( demon, params )
    if packed_params is None:
        return False

    return demon.InlineExecuteGetOutput( callback, "go", f"ObjectFiles/reg_query.{demon.ProcessArch}.o", packed_params )

def generic_callback( demonID, worked, output ):
    if worked:
        with open('/tmp/bof_output.txt', 'a'):
            f.write(output)

def sit_aw( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    demon  = Demon( demonID )

    return demon.InlineExecuteGetOutput( my_callback, "go", f"ObjectFiles/reg_query.{demon.ProcessArch}.o", b'' )

RegisterCommand( sit_aw, "", "sit-aw", "Get basic information about the current system", 0, "", "" )


def reg_query_recursive_parse_params( demon, params ):
    packer = SAPacker()

    reghives = {
        'HKCR': 0,
        'HKCU': 1,
        'HKLM': 2,
        'HKU': 3
    }

    num_params = len(params)
    params_parsed = 0

    if num_params < 2:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Missing parameters" )
        return None

    if num_params > 3:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return None

    if params[ params_parsed ].upper() not in reghives:
        hostname = params[ params_parsed ]
        params_parsed += 1
    else:
        hostname = None

    if params[ params_parsed ].upper() not in reghives:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Provided registry hive value is invalid" )
        return None

    hive = reghives[ params[ params_parsed ].upper() ]
    params_parsed += 1

    if num_params < params_parsed + 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Missing parameters" )
        return None

    path = params[ params_parsed ]

    key = None

    packer.addstr(hostname)
    packer.adduint32(hive)
    packer.addstr(path)
    packer.addstr(key)
    packer.addbool(True) # recursive

    return packer.getbuffer()

def reg_query_recursive( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = SAPacker()
    demon  = Demon( demonID )

    packed_params = reg_query_recursive_parse_params( demon, params )
    if packed_params is None:
        return False

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to query the windows registry recursively" )

    demon.InlineExecute( TaskID, "go", f"ObjectFiles/reg_query.{demon.ProcessArch}.o", packed_params, False )

    return TaskID

def wmi_query_parse_params( demon, params ):
    packer = SAPacker()

    query     = ''
    server    = '.'
    namespace = 'root\\cimv2'

    num_params = len(params)

    if num_params < 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Missing parameters" )
        return None

    if num_params > 3:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return None

    query = params[ 0 ]

    if num_params > 1:
        server = params[ 1 ]

    if num_params > 2:
        namespace = params[ 2 ]

    packer.addWstr(server)
    packer.addWstr(namespace)
    packer.addWstr(query)

    return packer.getbuffer()

def wmi_query( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    demon  = Demon( demonID )

    packed_params = wmi_query_parse_params( demon, params )
    if packed_params is None:
        return False

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to query the Windows Management Toolkit" )

    demon.InlineExecute( TaskID, "go", f"ObjectFiles/wmi_query.{demon.ProcessArch}.o", packed_params, False )

    return TaskID

def wmi_query_with_callback( demonID, callback, *params ):
    demon  : Demon  = None
    demon  = Demon( demonID )

    packed_params = wmi_query_parse_params( demon, params )
    if packed_params is None:
        return False

    return demon.InlineExecuteGetOutput( callback, "go", f"ObjectFiles/wmi_query.{demon.ProcessArch}.o", packed_params )

def nslookup_parse_params( demon, params ):
    packer = SAPacker()

    recordmapping = {
        'A': 1,
        'NS': 2,
        'MD': 3,
        'MF': 4,
        'CNAME': 5,
        'SOA': 6,
        'MB': 7,
        'MG': 8,
        'MR': 9,
        'WKS': 0xb,
        'PTR': 0xc,
        'HINFO': 0xd,
        'MINFO': 0xe,
        'MX': 0xf,
        'TEXT': 0x10,
        'RP': 0x11,
        'AFSDB': 0x12,
        'X25': 0x13,
        'ISDN': 0x14,
        'RT': 0x15,
        'AAAA': 0x1c,
        'SRV': 0x21,
        'WINSR': 0xff02,
        'KEY': 0x0019,
        'ANY': 0xff
    }

    num_params = len(params)
    lookup = ''
    server = ''
    _type   = recordmapping[ 'A' ]

    if num_params < 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Missing parameters" )
        return None

    lookup = params[ 0 ]

    if num_params > 1:
        server = params[ 1 ]
        if server == '127.0.0.1':
            demon.ConsoleWrite( demon.CONSOLE_ERROR, "Localhost dns query's have a potential to crash, refusing" )
            return None

    if num_params > 2 and params[ 2 ].upper() in recordmapping:
        _type = recordmapping[ params[ 2 ].upper() ]

    if num_params > 3:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return None

    packer.addstr(lookup)
    packer.addstr(server)
    packer.addshort(_type)

    return packer.getbuffer()

def nslookup( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    demon  = Demon( demonID )

    packed_params = nslookup_parse_params( demon, params )
    if packed_params is None:
        return False

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to run DNS query" )

    demon.InlineExecute( TaskID, "go", f"ObjectFiles/nslookup.{demon.ProcessArch}.o", packed_params, False )

    return TaskID

def env( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    demon  = Demon( demonID )

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to obtain the environment variables for the current process" )

    demon.InlineExecute( TaskID, "go", f"ObjectFiles/env.{demon.ProcessArch}.o", b'', False )

    return TaskID

def reg_query_with_callback( demonID, callback, *params ):
    demon  : Demon  = None
    demon  = Demon( demonID )

    packed_params = reg_query_parse_params( demon, params )
    if packed_params is None:
        return False

    return demon.InlineExecuteGetOutput( callback, "go", f"ObjectFiles/reg_query.{demon.ProcessArch}.o", packed_params )

def env_with_callback( demonID, callback, *params ):
    demon  : Demon  = None
    demon  = Demon( demonID )

    return demon.InlineExecuteGetOutput( callback, "go", f"ObjectFiles/env.{demon.ProcessArch}.o", b'' )

def get_password_policy_parse_params( demon, params ):
    packer = SAPacker()

    num_params = len(params)
    hostname = '.'

    if num_params == 1:
        hostname = params[ 0 ]

    if num_params > 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return None

    packer.addWstr(hostname)

    demon.InlineExecute( TaskID, "go", f"ObjectFiles/get_password_policy.{demon.ProcessArch}.o", packer.getbuffer(), False )

    return packer.getbuffer()

def get_password_policy( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    demon  = Demon( demonID )

    packed_params = get_password_policy_parse_params( demon, params )
    if packed_params is None:
        return False

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to obtain the password policy" )

    demon.InlineExecute( TaskID, "go", f"ObjectFiles/get_password_policy.{demon.ProcessArch}.o", packed_params, False )

    return TaskID

def list_firewall_rules( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = SAPacker()
    demon  = Demon( demonID )

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to list all firewall rules" )

    demon.InlineExecute( TaskID, "go", f"ObjectFiles/get_password_policy.{demon.ProcessArch}.o", b'', False )

    return TaskID

def cacls_parse_params( demon, params ):
    packer = SAPacker()

    num_params = len(params)

    if num_params < 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Not enough parameters" )
        return None

    filepath = params[ 0 ]

    if num_params > 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return None

    packer.addWstr(filepath)

    return packer.getbuffer()

def cacls( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    demon  = Demon( demonID )

    packed_params = cacls_parse_params( demon, params )
    if packed_params is None:
        return False

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to obtain file permissions" )

    demon.InlineExecute( TaskID, "go", f"ObjectFiles/cacls.{demon.ProcessArch}.o", packed_params, False )

    return TaskID

def schtasksenum_parse_params( demon, params ):
    packer = SAPacker()

    num_params = len(params)
    server = ''

    if num_params == 1:
        server = params[ 0 ]

    if num_params > 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return None

    packer.addWstr(server)

    return packer.getbuffer()

def schtasksenum( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    demon  = Demon( demonID )

    packed_params = schtasksenum_parse_params( demon, params )
    if packed_params is None:
        return False

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to list all scheduled tasks" )

    demon.InlineExecute( TaskID, "go", f"ObjectFiles/schtasksenum.{demon.ProcessArch}.o", packed_params, False )

    return TaskID

def schtasksquery_parse_params( demon, params ):
    packer = SAPacker()

    num_params = len(params)
    service = ''
    server = ''

    if num_params == 0:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Not enough parameters" )
        return None

    if num_params == 1:
        service = params[ 0 ]
    elif num_params == 2:
        server = params[ 0 ]
        service = params[ 1 ]
    else:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return None

    packer.addWstr(server)
    packer.addWstr(service)

    return packer.getbuffer()

def schtasksquery( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    demon  = Demon( demonID )

    packed_params = schtasksquery_parse_params( demon, params )
    if packed_params is None:
        return False

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to query a given scheduled task" )

    demon.InlineExecute( TaskID, "go", f"ObjectFiles/schtasksquery.{demon.ProcessArch}.o", packed_params, False )

    return TaskID

def sc_enum_parse_params( demon, params ):
    packer = SAPacker()

    num_params = len(params)
    server = ''

    if num_params == 1:
        server = params[ 0 ]

    if num_params > 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return None

    packer.addstr(server)

    return packer.getbuffer()

def sc_enum( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    demon  = Demon( demonID )

    packed_params = sc_enum_parse_params( demon, params )
    if packed_params is None:
        return False

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to enumerate all service configs" )

    demon.InlineExecute( TaskID, "go", f"ObjectFiles/sc_enum.{demon.ProcessArch}.o", packed_params, False )

    return TaskID

def sc_qc_parse_params( demon, params ):
    packer = SAPacker()

    num_params = len(params)
    service = ''
    server = ''

    if num_params == 0:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Not enough parameters" )
        return None

    if num_params == 1:
        service = params[ 0 ]
    elif num_params == 2:
        service = params[ 0 ]
        server = params[ 1 ]
    else:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return None

    packer.addstr(server)
    packer.addstr(service)

    return packer.getbuffer()

def sc_qc( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    demon  = Demon( demonID )

    packed_params = sc_qc_parse_params( demon, params )
    if packed_params is None:
        return False

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to run sc qc" )

    demon.InlineExecute( TaskID, "go", f"ObjectFiles/sc_qc.{demon.ProcessArch}.o", packed_params, False )

    return TaskID

def sc_query_parse_params( demon, params ):
    packer = SAPacker()

    num_params = len(params)
    service = ''
    server = ''

    if num_params == 0:
        pass
    elif num_params == 1:
        service = params[ 0 ]
    elif num_params == 2:
        service = params[ 0 ]
        server = params[ 1 ]
    else:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return None

    packer.addstr(server)
    packer.addstr(service)

    return packer.getbuffer()

def sc_query( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    demon  = Demon( demonID )

    packed_params = sc_query_parse_params( demon, params )
    if packed_params is None:
        return False

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to run sc query" )

    demon.InlineExecute( TaskID, "go", f"ObjectFiles/sc_query.{demon.ProcessArch}.o", packed_params, False )

    return TaskID

def sc_qdescription_parse_params( demon, params ):
    packer = SAPacker()

    num_params = len(params)
    service = ''
    server = ''

    if num_params == 0:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Not enough parameters" )
        return None

    if num_params == 1:
        service = params[ 0 ]
    elif num_params == 2:
        service = params[ 0 ]
        server = params[ 1 ]
    else:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return None

    packer.addstr(server)
    packer.addstr(service)

    return packer.getbuffer()

def sc_qdescription( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    demon  = Demon( demonID )

    packed_params = sc_qdescription_parse_params( demon, params )
    if packed_params is None:
        return False

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to get the description of a service" )

    demon.InlineExecute( TaskID, "go", f"ObjectFiles/sc_qdescription.{demon.ProcessArch}.o", packed_params, False )

    return TaskID

def sc_qfailure_get_params( demon, params ):
    packer = SAPacker()

    num_params = len(params)
    service = ''
    server = ''

    if num_params == 0:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Not enough parameters" )
        return None

    if num_params == 1:
        service = params[ 0 ]
    elif num_params == 2:
        service = params[ 0 ]
        server = params[ 1 ]
    else:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return None

    packer.addstr(server)
    packer.addstr(service)

    return packer.getbuffer()

def sc_qfailure( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    demon  = Demon( demonID )

    packed_params = sc_qfailure_get_params( demon, params )
    if packed_params is None:
        return False

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to get the failure reason for a service" )

    demon.InlineExecute( TaskID, "go", f"ObjectFiles/sc_qfailure.{demon.ProcessArch}.o", packed_params, False )

    return TaskID

def sc_qtriggerinfo_get_params( demon, params ):
    packer = SAPacker()

    num_params = len(params)
    service = ''
    server = ''

    if num_params == 0:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Not enough parameters" )
        return None

    if num_params == 1:
        service = params[ 0 ]
    elif num_params == 2:
        service = params[ 0 ]
        server = params[ 1 ]
    else:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return None

    packer.addstr(server)
    packer.addstr(service)

    return packer.getbuffer()

def sc_qtriggerinfo( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    demon  = Demon( demonID )

    packed_params = sc_qtriggerinfo_get_params( demon, params )
    if packed_params is None:
        return False

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to get the failure reason for a service" )

    demon.InlineExecute( TaskID, "go", f"ObjectFiles/sc_qtriggerinfo.{demon.ProcessArch}.o", packed_params, False )

    return TaskID

def adcs_enum_parse_params( demon, params ):
    packer = SAPacker()

    num_params = len(params)
    domain = ''

    if num_params > 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return None

    if num_params == 1:
        domain = params[ 0 ]

    packer.addWstr(domain)

    return packer.getbuffer()

def adcs_enum( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    demon  = Demon( demonID )

    packed_params = adcs_enum_parse_params( demon, params )
    if packed_params is None:
        return False

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to enumerate CAs and templates in the AD" )

    demon.InlineExecute( TaskID, "go", f"ObjectFiles/adcs_enum.{demon.ProcessArch}.o", packed_params, False )

    return TaskID

def enumlocalsessions( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    demon  = Demon( demonID )

    num_params = len(params)

    if num_params > 0:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return False

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to enumerate currently attached user sessions both local and over RDP" )

    demon.InlineExecute( TaskID, "go", f"ObjectFiles/enumlocalsessions.{demon.ProcessArch}.o", b'', False )

    return TaskID

def enumlocalsessions_with_callback( demonID, callback, *params ):
    demon  : Demon  = None
    demon  = Demon( demonID )

    num_params = len(params)

    if num_params > 0:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return False

    return demon.InlineExecuteGetOutput( callback, "go", f"ObjectFiles/enumlocalsessions.{demon.ProcessArch}.o", b'' )

def enum_filter_driver_parse_params( demon, params ):
    packer = SAPacker()

    num_params = len(params)
    system = ''

    if num_params > 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return None

    if num_params == 1:
        system = params[ 0 ]

    packer.addstr(system)

    return packer.getbuffer()

def enum_filter_driver( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    demon  = Demon( demonID )

    packed_params = enum_filter_driver_parse_params( demon, params )
    if packed_params is None:
        return False

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to enumerate filter drivers" )

    demon.InlineExecute( TaskID, "go", f"ObjectFiles/enum_filter_driver.{demon.ProcessArch}.o", packed_params, False )

    return TaskID

def ldapsearch_parse_params( demon, params ):
    packer = SAPacker()

    num_params = len(params)

    query = ''
    attributes = ''
    result_limit = 0
    hostname = ''
    domain = ''

    if num_params < 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Not enough parameters" )
        return None

    if num_params > 5:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return None

    query = params[ 0 ]

    if num_params >= 2:
        attributes = params[ 1 ]

    if num_params >= 3:
        result_limit = params[ 2 ]

    if num_params >= 4:
        hostname = params[ 3 ]

    if num_params >= 5:
        domain = params[ 4 ]

    packer.addstr(query)
    packer.addstr(attributes)
    packer.adduint32(result_limit)
    packer.addstr(hostname)
    packer.addstr(domain)

    return packer.getbuffer()

def ldapsearch( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    demon  = Demon( demonID )

    packed_params = ldapsearch_parse_params( demon, params )
    if packed_params is None:
        return False

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to run ldap query" )

    demon.InlineExecute( TaskID, "go", f"ObjectFiles/ldapsearch.{demon.ProcessArch}.o", packed_params, False )

    return TaskID

def netsession_parse_params( demon, params ):
    packer = SAPacker()

    num_params = len(params)
    computer = ''

    if num_params == 1:
        computer = params[ 0 ]
    elif num_params > 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return None

    packer.addWstr(computer)

    return packer.getbuffer()

def netsession( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    demon  = Demon( demonID )

    packed_params = netsession_parse_params( demon, params )
    if packed_params is None:
        return False

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to enumerate sessions on the local or specified computer" )

    demon.InlineExecute( TaskID, "go", f"ObjectFiles/get-netsession.{demon.ProcessArch}.o", packed_params, False )

    return TaskID

def netGroupList_parse_params( demon, params ):
    packer = SAPacker()

    num_params = len(params)
    domain = ''
    group = ''

    if num_params == 1:
        domain = params[ 0 ]
    elif num_params > 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return None

    packer.addshort(0)
    packer.addWstr(domain)
    packer.addWstr(group)

    return packer.getbuffer()

def netGroupList( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    demon  = Demon( demonID )

    packed_params = netGroupList_parse_params( demon, params )
    if packed_params is None:
        return False

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to list groups from the default or specified domain" )

    demon.InlineExecute( TaskID, "go", f"ObjectFiles/netgroup.{demon.ProcessArch}.o", packed_params, False )

    return TaskID

def netGroupListMembers_parse_params( demon, params ):
    packer = SAPacker()

    num_params = len(params)
    domain = ''
    group = ''

    if num_params < 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Not enough parameters" )
        return None
    elif num_params == 1:
        group = params[ 0 ]
    elif num_params == 2:
        domain = params[ 1 ]
    else:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return None

    packer.addshort(1)
    packer.addWstr(domain)
    packer.addWstr(group)

    return packer.getbuffer()

def netGroupListMembers( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    demon  = Demon( demonID )

    packed_params = netGroupListMembers_parse_params( demon, params )
    if packed_params is None:
        return False

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to list group members from the default or specified domain" )

    demon.InlineExecute( TaskID, "go", f"ObjectFiles/netgroup.{demon.ProcessArch}.o", packed_params, False )

    return TaskID

def netLocalGroupList_parse_params( demon, params ):
    packer = SAPacker()

    num_params = len(params)
    server = ''
    group = ''

    if num_params == 1:
        server = params[ 0 ]
    elif num_params > 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return None

    packer.addshort(0)
    packer.addWstr(server)
    packer.addWstr(group)

    return packer.getbuffer()

def netLocalGroupList( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    demon  = Demon( demonID )

    packed_params = netLocalGroupList_parse_params( demon, params )
    if packed_params is None:
        return False

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to list local groups from the local or specified computer" )

    demon.InlineExecute( TaskID, "go", f"ObjectFiles/netlocalgroup.{demon.ProcessArch}.o", packed_params, False )

    return TaskID

def netLclGrpLstMmbrs_parse_params( demon, params ):
    packer = SAPacker()

    num_params = len(params)
    domain = ''
    group = ''

    if num_params < 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Not enough parameters" )
        return None
    elif num_params == 1:
        group = params[ 0 ]
    elif num_params == 2:
        group = params[ 0 ]
        domain = params[ 1 ]
    else:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return None

    packer.addshort(1)
    packer.addWstr(domain)
    packer.addWstr(group)

    return packer.getbuffer()

def netLclGrpLstMmbrs( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    demon  = Demon( demonID )

    packed_params = netLclGrpLstMmbrs_parse_params( demon, params )
    if packed_params is None:
        return False

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to list local group members" )

    demon.InlineExecute( TaskID, "go", f"ObjectFiles/netlocalgroup.{demon.ProcessArch}.o", packed_params, False )

    return TaskID

def netuser_parse_params( demon, params ):
    packer = SAPacker()

    num_params = len(params)
    username = ''
    domain = ''

    if num_params < 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Not enough parameters" )
        return None
    elif num_params == 1:
        username = params[ 0 ]
    elif num_params == 2:
        username = params[ 0 ]
        domain = params[ 1 ]
    else:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return None

    packer.addWstr(username)
    packer.addWstr(domain)

    return packer.getbuffer()

def netuser( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    demon  = Demon( demonID )

    packed_params = netuser_parse_params( demon, params )
    if packed_params is None:
        return False

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to get info about specific user" )

    demon.InlineExecute( TaskID, "go", f"ObjectFiles/netuser.{demon.ProcessArch}.o", packed_params, False )

    return TaskID

def userenum_parse_parans( demon, params ):
    packer = SAPacker()

    num_params = len(params)

    enumtype = {
        'all': 1,
        'locked': 2,
        'disabled': 3,
        'active': 4
    }

    _type = enumtype[ 'all' ]

    if num_params == 1:
        if params[ 0 ].lower() not in enumtype:
            demon.ConsoleWrite( demon.CONSOLE_ERROR, "Parameter not in: [all, locked, disabled, active]" )
            return None
        _type = enumtype[ params[ 0 ].lower() ]
    elif num_params > 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return None

    packer.adduint32(0)
    packer.adduint32(_type)

    return packer.getbuffer()

def userenum( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    demon  = Demon( demonID )

    packed_params = userenum_parse_parans( demon, params )
    if packed_params is None:
        return False

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to list user accounts on the current computer" )

    demon.InlineExecute( TaskID, "go", f"ObjectFiles/netuserenum.{demon.ProcessArch}.o", packed_params, False )

    return TaskID

def userenum_with_callback( demonID, callback, *params ):
    demon  : Demon  = None
    demon  = Demon( demonID )

    packed_params = userenum_parse_parans( demon, params )
    if packed_params is None:
        return False

    return demon.InlineExecuteGetOutput( callback, "go", f"ObjectFiles/netuserenum.{demon.ProcessArch}.o", packed_params )

def domainenum_parse_params( demon, params ):
    packer = SAPacker()

    num_params = len(params)

    enumtype = {
        'all': 1,
        'locked': 2,
        'disabled': 3,
        'active': 4
    }

    _type = enumtype[ 'all' ]

    if num_params == 1:
        if params[ 0 ].lower() not in enumtype:
            demon.ConsoleWrite( demon.CONSOLE_ERROR, "Parameter not in: [all, locked, disabled, active]" )
            return None
        _type = enumtype[ params[ 0 ].lower() ]
    elif num_params > 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return None

    packer.adduint32(1)
    packer.adduint32(_type)

    return packer.getbuffer()

def domainenum( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    demon  = Demon( demonID )

    packed_params = domainenum_parse_params( demon, params )
    if packed_params is None:
        return False

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to list user accounts in the current domain" )

    demon.InlineExecute( TaskID, "go", f"ObjectFiles/netuserenum.{demon.ProcessArch}.o", packed_params, False )

    return TaskID

def netshares_parse_params( demon, params ):
    packer = SAPacker()

    num_params = len(params)
    computer = ''

    if num_params == 1:
        computer = params[ 0 ]
    elif num_params > 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return False

    packer.addWstr(computer)
    packer.adduint32(0)

    return packer.getbuffer()

def netshares( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    demon  = Demon( demonID )

    packed_params = netshares_parse_params( demon, params )
    if packed_params is None:
        return False

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to list shares on local or remote computer" )

    demon.InlineExecute( TaskID, "go", f"ObjectFiles/netshares.{demon.ProcessArch}.o", packed_params, False )

    return TaskID

def netsharesAdmin_parse_params( demon, params ):
    packer = SAPacker()

    num_params = len(params)
    computer = ''

    if num_params == 1:
        computer = params[ 0 ]
    elif num_params > 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return None

    packer.addWstr(computer)
    packer.adduint32(1)

    return packer.getbuffer()

def netsharesAdmin( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    demon  = Demon( demonID )

    packed_params = netsharesAdmin_parse_params( demon, params )
    if packed_params is None:
        return False

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to list shares on local or remote computer" )

    demon.InlineExecute( TaskID, "go", f"ObjectFiles/netshares.{demon.ProcessArch}.o", packed_params, False )

    return TaskID

def netuptime_parse_params( demon, params ):
    packer = SAPacker()

    num_params = len(params)
    hostname = ''

    if num_params == 1:
        hostname = params[ 0 ]
    elif num_params > 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return None

    packer.addWstr(hostname)

    return packer.getbuffer()

def netuptime( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    demon  = Demon( demonID )

    packed_params = netuptime_parse_params( demon, params )
    if packed_params is None:
        return False

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to list local workstations and servers" )

    demon.InlineExecute( TaskID, "go", f"ObjectFiles/netuptime.{demon.ProcessArch}.o", packed_params, False )

    return TaskID

def netview_parse_params( demon, params ):
    packer = SAPacker()

    num_params = len(params)
    computer = ''

    if num_params == 1:
        computer = params[ 0 ]
    elif num_params > 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return None

    packer.addWstr(computer)

    return packer.getbuffer()

def netview( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    demon  = Demon( demonID )

    packed_params = netview_parse_params( demon, params )
    if packed_params is None:
        return False

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to list local workstations and servers" )

    demon.InlineExecute( TaskID, "go", f"ObjectFiles/netview.{demon.ProcessArch}.o", packed_params, False )

    return TaskID

def quser_parse_params( demon, params ):
    packer = SAPacker()

    num_params = len(params)
    hostname   = ''

    if num_params < 1:
        hostname = '127.0.0.1'
    elif num_params == 1:
        hostname = params[ 0 ]
    elif num_params > 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return None

    packer.addstr(hostname)

    return packer.getbuffer()

def quser( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    demon  = Demon( demonID )

    packed_params = quser_parse_params( demon, params )
    if packed_params is None:
        return False

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, f"Tasked demon to obtain the list RDP connections on {hostname}" )

    demon.InlineExecute( TaskID, "go", f"ObjectFiles/quser.{demon.ProcessArch}.o", packed_params, False )

    return TaskID

def bofdir_parse_params( demon, params ):
    packer = SAPacker()

    num_params = len(params)
    targetdir  = '.\\'
    subdirs    = 0

    if num_params > 2:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return None

    if num_params > 0:
        targetdir = params[0]

    if num_params == 2 and params[1] != '/s':
        demon.ConsoleWrite( demon.CONSOLE_ERROR, f"Invalid parameter: {params[1]}" )
        return None

    if num_params == 2 and params[1] == '/s':
        subdirs = 1

    packer.addWstr(targetdir)
    packer.addshort(subdirs)

    return packer.getbuffer()

def bofdir( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    demon  = Demon( demonID )

    packed_params = bofdir_parse_params( demon, params )
    if packed_params is None:
        return False

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, f"Tasked demon to list a directory" )

    demon.InlineExecute( TaskID, "go", f"ObjectFiles/dir.{demon.ProcessArch}.o", packed_params, False )

    return TaskID

def bofdir_with_callback( demonID, callback, *params ):
    demon  : Demon  = None
    demon  = Demon( demonID )

    packed_params = bofdir_parse_params( demon, params )
    if packed_params is None:
        return False

    return demon.InlineExecuteGetOutput( callback, "go", f"ObjectFiles/dir.{demon.ProcessArch}.o", packed_params )

def tasklist_parse_params( demon, params ):
    packer = SAPacker()

    num_params = len(params)
    hostname   = ''

    if num_params > 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return None

    if num_params > 0:
        hostname = params[0]

    packer.addWstr(hostname)

    return packer.getbuffer()

def tasklist( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    demon  = Demon( demonID )

    packed_params = tasklist_parse_params( demon, params )
    if packed_params is None:
        return False

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, f"Tasked demon list running processes" )

    demon.InlineExecute( TaskID, "go", f"ObjectFiles/tasklist.{demon.ProcessArch}.o", packed_params, False )

    return TaskID

def tasklist_with_callback( demonID, callback, *params ):
    demon  : Demon  = None
    demon  = Demon( demonID )

    packed_params = tasklist_parse_params( demon, params )
    if packed_params is None:
        return False

    return demon.InlineExecuteGetOutput( callback, "go", f"ObjectFiles/tasklist.{demon.ProcessArch}.o", packed_params )

def callback_output_failed(bof_output):
    return bof_output['worked'] is False or bof_output['error'] != '' or bof_output['output'] == ''

def os_info(bof_output):
    info = {}

    bof_num = 0

    if callback_output_failed(bof_output[bof_num]):
        info['ProductName'] = '?'
    else:
        info['ProductName'] = bof_output[bof_num]['output'].split('REG_SZ')[1].strip()

    bof_num += 1

    if callback_output_failed(bof_output[bof_num]):
        info['ReleaseId'] = '?'
    else:
        info['ReleaseId'] = bof_output[bof_num]['output'].split(' ')[-1].strip()

    bof_num += 1

    if callback_output_failed(bof_output[bof_num]):
        info['CurrentMajorVersionNumber'] = '?'
    else:
        info['CurrentMajorVersionNumber'] = bof_output[bof_num]['output'].split(' ')[-1].strip()

    bof_num += 1

    if callback_output_failed(bof_output[bof_num]):
        info['CurrentVersion'] = '?'
    else:
        info['CurrentVersion'] = bof_output[bof_num]['output'].split(' ')[-1].strip()

    bof_num += 1

    if callback_output_failed(bof_output[bof_num]):
        info['CurrentBuildNumber'] = '?'
    else:
        info['CurrentBuildNumber'] = bof_output[bof_num]['output'].split(' ')[-1].strip()

    bof_num += 1

    if callback_output_failed(bof_output[bof_num]):
        info['arch'] = '?'
    else:
        match = re.search(r'PROCESSOR_ARCHITECTURE=(.*)', bof_output[bof_num]['output'])
        if match is not None:
            info['arch'] = match.group(1)
        else:
            info['arch'] = '?'

    bof_num += 1

    if callback_output_failed(bof_output[bof_num]):
        info['ip'] = '?'
        info['DNS'] = '?'
    else:
        match = re.search(r'\s+(.+)\nHostname:', bof_output[bof_num]['output'], re.MULTILINE)
        if match is not None:
            info['ip'] = match.group(1)
        else:
            info['ip'] = '?'

        match = re.search(r'DNS Server:\s+(.*)', bof_output[bof_num]['output'])
        if match is not None:
            info['DNS'] = match.group(1)
        else:
            info['DNS'] = '?'

    bof_num += 1

    if callback_output_failed(bof_output[bof_num]):
        info['Domain'] = '?'
    else:
        match = re.search(r'Domain\n(.*)', bof_output[bof_num]['output'])
        if match is not None:
            info['Domain'] = match.group(1)
        else:
            info['Domain'] = '?'

    bof_num += 1

    info['manufacturer'] = '?'
    info['model'] = '?'

    bof_num += 1

    if callback_output_failed(bof_output[bof_num]):
        info['uptime'] = '?'
    else:
        match = re.search(r'Uptime: (.*)', bof_output[bof_num]['output'])
        if match is not None:
            info['uptime'] = match.group(1)
        else:
            info['uptime'] = '?'

    return info

def user_info(bof_output):
    info = {}

    bof_num = 10

    if callback_output_failed(bof_output[bof_num]):
        info['username'] = '?'
        info['integrity'] = '?'
        info['groups'] = ['?']
        info['isLocalAdmin'] = '?'
        info['privs'] = ['?']
        info['isadmin'] = '?'
    else:
        match = re.search(r'UserName\s+SID\s*\n[=\s]+\n(.*?)\s*S-', bof_output[bof_num]['output'])
        if match is not None:
            info['username'] = match.group(1)
        else:
            info['username'] = '?'

        match = re.search(r'Mandatory Label\\(\S+)', bof_output[bof_num]['output'])
        if match is not None:
            info['integrity'] = match.group(1)
        else:
            info['integrity'] = '?'

        info['groups'] = re.findall(r'^(.+?)\s*(?:Well-known group|Group|Alias)',  bof_output[bof_num]['output'], re.MULTILINE)
        info['isLocalAdmin'] = 'S-1-5-32-544' in  bof_output[bof_num]['output']
        info['privs'] = re.findall(r'(Se\S*).*Enabled\s*', bof_output[bof_num]['output'])
        info['isadmin'] = False # TODO: add

    return info

def ps_info(bof_output):
    info = {}

    bof_num = 11

    info['CLRs'] = []
    info['versions'] = []

    if callback_output_failed(bof_output[bof_num]) is False:
        info['CLRs'].append('v1.0.3705')

    bof_num += 1

    if callback_output_failed(bof_output[bof_num]) is False:
        info['CLRs'].append('v1.1.4322')

    bof_num += 1

    if callback_output_failed(bof_output[bof_num]) is False:
        info['CLRs'].append('v2.0.50727')

    bof_num += 1

    if callback_output_failed(bof_output[bof_num]) is False:
        info['CLRs'].append('v3.0')

    bof_num += 1

    if callback_output_failed(bof_output[bof_num]) is False:
        info['CLRs'].append('v3.5')

    bof_num += 1

    if callback_output_failed(bof_output[bof_num]) is False:
        info['CLRs'].append('v4.0.30319')

    bof_num += 1

    if callback_output_failed(bof_output[bof_num]) is False:
        info['versions'].append(bof_output[bof_num]['output'].split('REG_SZ')[1].strip())

    bof_num += 1

    if callback_output_failed(bof_output[bof_num]) is False:
        info['versions'].append(bof_output[bof_num]['output'].split('REG_SZ')[1].strip())

    bof_num += 1

    # TODO: test these regexes in a Windows machine with logging enabled
    if callback_output_failed(bof_output[bof_num]):
        info['EnableTranscripting'] = False
    else:
        match = re.search(r'EnableTranscripting\s+\w+\s+(\d+)', bof_output[bof_num]['output'])
        if match is not None:
            info['EnableTranscripting'] = int(match.group(1)) == 1
        else:
            info['EnableTranscripting'] = False

    bof_num += 1

    if callback_output_failed(bof_output[bof_num]):
        info['EnableInvocationHeader'] = False
    else:
        match = re.search(r'EnableInvocationHeader\s+\w+\s+(\d+)', bof_output[bof_num]['output'])
        if match is not None:
            info['EnableInvocationHeader'] = int(match.group(1)) == 1
        else:
            info['EnableInvocationHeader'] = False

    bof_num += 1

    if callback_output_failed(bof_output[bof_num]):
        info['EnableModuleLogging'] = False
    else:
        match = re.search(r'EnableModuleLogging\s+\w+\s+(\d+)', bof_output[bof_num]['output'])
        if match is not None:
            info['EnableModuleLogging'] = int(match.group(1)) == 1
        else:
            info['EnableModuleLogging'] = False

    bof_num += 1

    if callback_output_failed(bof_output[bof_num]):
        info['EnableScriptBlockLogging'] = False
    else:
        match = re.search(r'EnableScriptBlockLogging\s+\w+\s+(\d+)', bof_output[bof_num]['output'])
        if match is not None:
            info['EnableScriptBlockLogging'] = int(match.group(1)) == 1
        else:
            info['EnableScriptBlockLogging'] = False

    bof_num += 1

    if callback_output_failed(bof_output[bof_num]):
        info['EnableScriptBlockInvocationLogging'] = False
    else:
        match = re.search(r'EnableScriptBlockInvocationLogging\s+\w+\s+(\d+)', bof_output[bof_num]['output'])
        if match is not None:
            info['EnableScriptBlockInvocationLogging'] = int(match.group(1)) == 1
        else:
            info['EnableScriptBlockInvocationLogging'] = False

    return info

def dotnet_info(bof_output):
    info = {}

    info['CLR'] = {}
    info['.NET'] = {}
    info['CLR']['versions'] = []
    info['.NET']['versions'] = []

    bof_num = 24

    if callback_output_failed(bof_output[bof_num]):
        info['CLR']['versions'] = ['?']
    else:
        info['CLR']['versions'] = re.findall(r'<dir> (v.*)', bof_output[bof_num]['output'])

    bof_num += 1

    if callback_output_failed(bof_output[bof_num]) is False:
        match = re.search(r'\s+Version\s+REG_SZ\s+(.*)', bof_output[bof_num]['output'])
        if match is not None:
            info['.NET']['versions'].append(match.group(1))

    bof_num += 1

    if callback_output_failed(bof_output[bof_num]) is False:
        match = re.search(r'\s+Version\s+REG_SZ\s+(.*)', bof_output[bof_num]['output'])
        if match is not None:
            info['.NET']['versions'].append(match.group(1))

    return info

def avedr_info(bof_output):
    info = {}

    bof_num = 27

    if callback_output_failed(bof_output[bof_num]):
        info['AVs'] = []
    else:
        data = bof_output[bof_num].split('displayName, instanceGuid')
        if len(bof_output) != 2:
            return info
        data = data[1]
        data = data.split('\n\n')
        if len(bof_output) < 2:
            return info
        data = data[0]
        info['AVs'] = re.findall(r'^([^,]+), .+?, .+?, ([^,]+), ', data, re.MULTILINE)

    return info

def processes_info(bof_output):
    info = {}

    bof_num = 28

    info['names'] = []
    info['browser']     = []
    info['interesting'] = []
    info['defensive']   = []

    if callback_output_failed(bof_output[bof_num]) is False:
        data = bof_output[bof_num]['output']
        data = data.split('\n')[1:]
        for entry in data:
            match = re.search(r'^(.*?)\s+\d', entry)
            if match is not None:
                info['names'].append(match.group(1))

        proctypes = ['browser', 'interesting', 'defensive']
        for proctype in proctypes:
            info[proctype] = {}
            with open(os.path.join(os.path.dirname(os.path.realpath('__file__')), 'client/Modules/SituationalAwareness/', f'{proctype}.json')) as f:
                j = json.load(f)
            for type_example in j:
                for proc in info['names']:
                    if type_example == proc.replace('.exe', ''):
                        info[proctype][proc] = j[type_example]

    return info

def uac_info(bof_output):
    info = {}

    bof_num = 29

    if callback_output_failed(bof_output[bof_num]):
        info['ConsentPromptBehaviorAdmin'] = '?'
    else:
        match = re.search(r'ConsentPromptBehaviorAdmin\s+REG_DWORD\s+(\d+)', bof_output[bof_num]['output'])
        if match is not None:
            info['ConsentPromptBehaviorAdmin'] = int(match.group(1))
        else:
            info['ConsentPromptBehaviorAdmin'] = '?'

    bof_num += 1

    if callback_output_failed(bof_output[bof_num]):
        info['EnableLUA'] = False
    else:
        match = re.search(r'EnableLUA\s+REG_DWORD\s+(\d+)', bof_output[bof_num]['output'])
        if match is not None:
            info['EnableLUA'] = int(match.group(1)) == 1
        else:
            info['EnableLUA'] = False

    bof_num += 1

    if callback_output_failed(bof_output[bof_num]):
        info['LocalAccountTokenFilterPolicy'] = False
    else:
        match = re.search(r'LocalAccountTokenFilterPolicy\s+REG_DWORD\s+(\d+)', bof_output[bof_num]['output'])
        if match is not None:
            info['LocalAccountTokenFilterPolicy'] = int(match.group(1)) == 1
        else:
            info['LocalAccountTokenFilterPolicy'] = False

    bof_num += 1

    if callback_output_failed(bof_output[bof_num]):
        info['FilterAdministratorToken'] = False
    else:
        match = re.search(r'FilterAdministratorToken\s+REG_DWORD\s+(\d+)', bof_output[bof_num]['output'])
        if match is not None:
            info['FilterAdministratorToken'] = int(match.group(1)) == 1
        else:
            info['FilterAdministratorToken'] = False

    return info

def local_users_info(bof_output):
    info = {}

    bof_num = 33

    if callback_output_failed(bof_output[bof_num]):
        info['local_users'] = ['?']
    else:
        info['local_users'] = re.findall(rf'^-- (.*)$', bof_output[bof_num]['output'], re.MULTILINE)

    return info

def local_sessions_info(bof_output):
    info = {}

    bof_num = 34

    if callback_output_failed(bof_output[bof_num]):
        info['local_sessions'] = ['?']
    else:
        info['local_sessions'] = re.findall(r'^  - \[\d\] (.*?)$', bof_output[bof_num]['output'], re.MULTILINE)

    return info

def open_windows_info(bof_output):
    info = {}

    bof_num = 35

    if callback_output_failed(bof_output[bof_num]):
        info['open_windows'] = ['?']
    else:
        data = bof_output[bof_num]['output']
        data = data.split('\n')
        info['open_windows'] = [entry for entry in data if entry != '']

    return info

def bofbelt_report( demonID, bof_output ):
    demon  : Demon  = None
    demon  = Demon( demonID )

    report = {}
    report['os']             = os_info(bof_output)
    report['user']           = user_info(bof_output)
    report['ps']             = ps_info(bof_output)
    report['dotnet']         = dotnet_info(bof_output)
    report['avedr']          = avedr_info(bof_output)
    report['processes']      = processes_info(bof_output)
    report['uac']            = uac_info(bof_output)
    report['local_users']    = local_users_info(bof_output)
    report['local_sessions'] = local_sessions_info(bof_output)
    report['open_windows']   = open_windows_info(bof_output)
    #print(json.dumps(bof_output, indent=2))
    #print(json.dumps(report, indent=2))

    # OS

    try:
        demon.ConsoleWrite( demon.CONSOLE_INFO, "OS Information" )
        demon.ConsoleWrite( demon.CONSOLE_INFO, f"OS           : {report['os']['ProductName']}" )
        demon.ConsoleWrite( demon.CONSOLE_INFO, f"Version      : max:{report['os']['CurrentMajorVersionNumber']}, min:{report['os']['CurrentVersion']}" )
        demon.ConsoleWrite( demon.CONSOLE_INFO, f"Build        : {report['os']['CurrentBuildNumber']}" )
        demon.ConsoleWrite( demon.CONSOLE_INFO, f"Arch         : {report['os']['arch']}" )
        demon.ConsoleWrite( demon.CONSOLE_INFO, f"IP           : {report['os']['ip']}" )
        demon.ConsoleWrite( demon.CONSOLE_INFO, f"DNS          : {report['os']['DNS']}" )
        demon.ConsoleWrite( demon.CONSOLE_INFO, '')
    except Exception as e:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, f"Error obtaining OS Information: {e}" )

    # user

    try:
        demon.ConsoleWrite( demon.CONSOLE_INFO, "User Information" )
        demon.ConsoleWrite( demon.CONSOLE_INFO, f"Username        : {report['user']['username']}" )
        isLocalAdmin_text = 'Yes' if report['user']['isLocalAdmin'] else 'No'
        integrity_text = report['user']['integrity']
        if report['user']['isLocalAdmin'] and report['user']['integrity'] == 'Medium':
            integrity_text += '[!] In medium integrity but user is a local administrator - UAC can be bypassed.'
        demon.ConsoleWrite( demon.CONSOLE_INFO, f"IsLocalAdmin    : {isLocalAdmin_text}" )
        demon.ConsoleWrite( demon.CONSOLE_INFO, f"Integrity Level : {integrity_text}" )
        demon.ConsoleWrite( demon.CONSOLE_INFO, f"Group memberships" )
        for group in report['user']['groups']:
            demon.ConsoleWrite( demon.CONSOLE_INFO, f' - {group}' )
        demon.ConsoleWrite( demon.CONSOLE_INFO, f"Privileges" )
        for priv in report['user']['privs']:
            demon.ConsoleWrite( demon.CONSOLE_INFO, f' - {priv}' )
        demon.ConsoleWrite( demon.CONSOLE_INFO, f'' )
    except Exception as e:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, f"Error obtaining User Information: {e}" )

    # powershell

    try:
        demon.ConsoleWrite( demon.CONSOLE_INFO, "PowerShell Information" )
        osSupportsAmsi = int(report['os']['CurrentMajorVersionNumber']) >= 10
        supported_text = 'Yes' if osSupportsAmsi else 'No'
        demon.ConsoleWrite( demon.CONSOLE_INFO, f"AMSI support: {supported_text}" )
        demon.ConsoleWrite( demon.CONSOLE_INFO, f"CLRs installed" )
        for clr in report['ps']['CLRs']:
            demon.ConsoleWrite( demon.CONSOLE_INFO, f' - {clr[1:]}' )
        demon.ConsoleWrite( demon.CONSOLE_INFO, f"Versions installed" )
        for ver in report['ps']['versions']:
            if ver == '2.0':
                if 'v2.0.50727' not in report['ps']['CLRs']:
                    ver += ' [!] Version 2.0.50727 of the CLR is not installed - PowerShell v2.0 won\'t be able to run.'
                elif osSupportsAmsi:
                    ver += ' [!] This version does not support AMSI'
            demon.ConsoleWrite( demon.CONSOLE_INFO, f' - {ver}' )
        demon.ConsoleWrite( demon.CONSOLE_INFO, f'Transcription Logging Settings' )
        demon.ConsoleWrite( demon.CONSOLE_INFO, f'    Enabled            : {report["ps"]["EnableTranscripting"]}')
        demon.ConsoleWrite( demon.CONSOLE_INFO, f'    Invocation Logging : {report["ps"]["EnableInvocationHeader"]}')
        demon.ConsoleWrite( demon.CONSOLE_INFO, 'Module Logging Settings')
        demon.ConsoleWrite( demon.CONSOLE_INFO, f'    Enabled            : {report["ps"]["EnableModuleLogging"]}')
        demon.ConsoleWrite( demon.CONSOLE_INFO, 'Script Block Logging Settings')
        demon.ConsoleWrite( demon.CONSOLE_INFO, f'    Enabled            : {report["ps"]["EnableScriptBlockLogging"]}')
        demon.ConsoleWrite( demon.CONSOLE_INFO, f'    Invocation Logging : {report["ps"]["EnableScriptBlockInvocationLogging"]}')
        demon.ConsoleWrite( demon.CONSOLE_INFO, '')
    except Exception as e:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, f"Error obtaining PowerShell Information: {e}" )

    # .NET

    try:
        demon.ConsoleWrite( demon.CONSOLE_INFO, '.NET Information')
        latest_version = report['dotnet']['.NET']['versions'][-1]
        highestVersion_Major = int(latest_version.split('.')[0])
        highestVersion_Minor = int(latest_version.split('.')[1])
        supports_amsi = highestVersion_Major > 4 or (highestVersion_Major == 4 and highestVersion_Minor >= 8)
        supported_text = 'Yes' if supports_amsi else 'No'
        demon.ConsoleWrite( demon.CONSOLE_INFO, f'AMSI support: {supported_text}')
        demon.ConsoleWrite( demon.CONSOLE_INFO, 'CLRs installed')
        for clr in report['ps']['CLRs']:
            demon.ConsoleWrite( demon.CONSOLE_INFO, f' - {clr[1:]}')
        demon.ConsoleWrite( demon.CONSOLE_INFO, '.NET versions installed')
        for ver in report['dotnet']['.NET']['versions']:
            high = int(ver.split('.')[0])
            low = int(ver.split('.')[1])
            if (high < 4 or (high == 4 and low < 8)) and supports_amsi:
                ver += ' [!] This version does not support AMSI'
            demon.ConsoleWrite( demon.CONSOLE_INFO, f' - {ver}')
        demon.ConsoleWrite( demon.CONSOLE_INFO, '')
    except Exception as e:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, f'Error obtaining .NET Information: {e}')

    # AV/EDR

    try:
        demon.ConsoleWrite( demon.CONSOLE_INFO, ('AVs/EDRs Information'))
        for name, path in report['avedr']['AVs']:
            demon.ConsoleWrite( demon.CONSOLE_INFO, f' - {name}, {path}')
        if len(report['avedr']['AVs']) == 0:
            demon.ConsoleWrite( demon.CONSOLE_INFO, '- None found')
        demon.ConsoleWrite( demon.CONSOLE_INFO, '')
    except Exception as e:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, f'Error obtaining AVs/EDRs Information: {e}')

    # processes

    try:
        demon.ConsoleWrite( demon.CONSOLE_INFO, 'Processes Information')
        # TODO: add PID
        proctypes = ['browser', 'interesting', 'defensive']
        submenus = ['Browsers', 'Interesting processes', 'Defensive processes']
        for i in range(len(proctypes)):
            proctype = proctypes[i]
            submenu = submenus[i]
            if len(report['processes'][proctype]) == 0:
                continue
            demon.ConsoleWrite( demon.CONSOLE_INFO, submenu)
            for elem in report['processes'][proctype]:
                demon.ConsoleWrite( demon.CONSOLE_INFO, f' - {elem} -> {report["processes"][proctype][elem]}')
        demon.ConsoleWrite( demon.CONSOLE_INFO, '')
    except Exception as e:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, f'Error obtaining Processes Information: {e}')

    # UAC

    try:
        demon.ConsoleWrite( demon.CONSOLE_INFO, 'UAC Information')
        meaning = {
            '': 'PromptForNonWindowsBinaries',
            0: 'No prompting',
            1: 'PromptOnSecureDesktop',
            2: 'PromptPermitDenyOnSecureDesktop',
            3: 'PromptForCredsNotOnSecureDesktop',
            4: 'PromptForPermitDenyNotOnSecureDesktop',
            5: 'PromptForNonWindowsBinaries'
        }
        demon.ConsoleWrite( demon.CONSOLE_INFO, f'ConsentPromptBehaviorAdmin    : {report["uac"]["ConsentPromptBehaviorAdmin"]} - {meaning[report["uac"]["ConsentPromptBehaviorAdmin"]]}')
        text = 'Yes' if report['uac']['EnableLUA'] else 'No'
        demon.ConsoleWrite( demon.CONSOLE_INFO, f'EnableLUA (Is UAC enabled?)   : {text}')
        text = 'Yes' if report['uac']['LocalAccountTokenFilterPolicy'] else 'No'
        demon.ConsoleWrite( demon.CONSOLE_INFO, f'LocalAccountTokenFilterPolicy : {text}')
        text = 'Yes' if report['uac']['FilterAdministratorToken'] else 'No'
        demon.ConsoleWrite( demon.CONSOLE_INFO, f'FilterAdministratorToken      : {text}')
        if report['uac']['EnableLUA'] is False:
            demon.ConsoleWrite( demon.CONSOLE_INFO, '[*] UAC is disabled. Any administrative local account can be used for lateral movement.')
        else:
            if report['uac']['LocalAccountTokenFilterPolicy'] is False and report['uac']['FilterAdministratorToken'] is False:
                demon.ConsoleWrite( demon.CONSOLE_INFO, '[*] Default Windows settings - Only the RID-500 local admin account can be used for lateral movement.')
            elif report['uac']['LocalAccountTokenFilterPolicy'] is True:
                demon.ConsoleWrite( demon.CONSOLE_INFO, '[*] LocalAccountTokenFilterPolicy == 1. Any administrative local account can be used for lateral movement.')
            else:
                demon.ConsoleWrite( demon.CONSOLE_INFO, '[*] LocalAccountTokenFilterPolicy set to 0 and FilterAdministratorToken == 1. Local accounts cannot be used for lateral movement.')
        demon.ConsoleWrite( demon.CONSOLE_INFO, '')
    except Exception as e:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, f'Error obtaining UAC Information: {e}')

    # Local users

    try:
        demon.ConsoleWrite( demon.CONSOLE_INFO, 'Local Users Information')
        usernames = report['local_users']['local_users']
        num_users = len(usernames)
        max_num = 10
        if num_users > max_num:
            usernames = usernames[:max_num]
            demon.ConsoleWrite( demon.CONSOLE_INFO, f'Only showing {max_num} users of {num_users}. Run \'userenum\' to get the full list.')
        if num_users == 0:
            demon.ConsoleWrite( demon.CONSOLE_INFO, f'No users found')
        for username in usernames:
            demon.ConsoleWrite( demon.CONSOLE_INFO, f'  - {username}')
        demon.ConsoleWrite( demon.CONSOLE_INFO, '')
    except Exception as e:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, f'Error obtaining Local Users Information: {e}')

    # Local sessions

    try:
        demon.ConsoleWrite( demon.CONSOLE_INFO, 'Local Sessions Information')
        sessions = report['local_sessions']['local_sessions']
        num_sessions = len(sessions)
        max_num = 10
        if num_sessions > max_num:
            sessions = sessions[:max_num]
            demon.ConsoleWrite( demon.CONSOLE_INFO, f'Only showing {max_num} session of {num_sessions}. Run \'enumLocalSessions\' to get the full list.')
        if num_sessions == 0:
            demon.ConsoleWrite( demon.CONSOLE_INFO, f'No sessions found')
        for session in sessions:
            demon.ConsoleWrite( demon.CONSOLE_INFO, f'  - {session}')
        demon.ConsoleWrite( demon.CONSOLE_INFO, '')
    except Exception as e:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, f'Error obtaining Local Sessions Information: {e}')

    try:
        demon.ConsoleWrite( demon.CONSOLE_INFO, 'Open windows Information')
        windows = report['open_windows']['open_windows']
        num_windows = len(windows)
        max_num = 10
        if num_windows > max_num:
            windows = windows[:max_num]
            demon.ConsoleWrite( demon.CONSOLE_INFO, f'Only showing {max_num} windows of {num_windows}. Run \'windowlist\' to get the full list.')
        if num_windows == 0:
            demon.ConsoleWrite( demon.CONSOLE_INFO, f'No windows found')
        for window in windows:
            demon.ConsoleWrite( demon.CONSOLE_INFO, f'  - {window}')
        demon.ConsoleWrite( demon.CONSOLE_INFO, '')
    except Exception as e:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, f'Error obtaining Open windows Information: {e}')

# this callback is triggered by every BOF
# demonID: the ID of the demon that ran the BOF
# TaskID : the ID of the task returned by demon.InlineExecuteGetOutput
# worked : weather the BOF was able to run or not
# output : the content of all CALLBACK_OUTPUT
# error  : the content of all CALLBACK_ERROR
def bofbelt_callback( demonID, TaskID, worked, output, error ):
    filename = '/tmp/bofbelt.json'

    # first, get the json that contains all the previous BOF output
    try:
        with open(filename, 'r') as f:
            bof_output = json.load(f)
    except:
        bof_output = []

    # add the data for this BOF callback
    bof_output.append({
        'worked': worked,
        'TaskID': TaskID,
        'output': output,
        'error' : error
    })

    # save all the data
    with open(filename, 'w') as f:
        f.write(json.dumps(bof_output))

    # get how many BOFs have completed
    num_entries  = len(bof_output)

    # are we done?
    if num_entries == 36:
        os.remove(filename)
        bofbelt_report( demonID, bof_output )

    return True

def bofbelt( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    demon  = Demon( demonID )

    # Getting basic OS information
    reg_query_with_callback( demonID, bofbelt_callback, "HKLM", "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion", "ProductName" )
    reg_query_with_callback( demonID, bofbelt_callback, "HKLM", "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion", "ReleaseId" )
    reg_query_with_callback( demonID, bofbelt_callback, "HKLM", "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion", "CurrentMajorVersionNumber" )
    reg_query_with_callback( demonID, bofbelt_callback, "HKLM", "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion", "CurrentVersion" )
    reg_query_with_callback( demonID, bofbelt_callback, "HKLM", "SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion", "CurrentBuildNumber" )
    env_with_callback( demonID, bofbelt_callback )
    ipconfig_with_callback( demonID, bofbelt_callback )
    wmi_query_with_callback( demonID, bofbelt_callback, "Select Domain from Win32_ComputerSystem" )
    wmi_query_with_callback( demonID, bofbelt_callback, "Select * from Win32_ComputerSystem" )
    uptime_with_callback( demonID, bofbelt_callback )

    # Getting User information

    whoami_with_callback( demonID, bofbelt_callback )

    # Getting PowerShell information

    bofdir_with_callback( demonID, bofbelt_callback, 'C:\\Windows\\Microsoft.Net\\Framework\\v1.0.3705\\System.dll' )
    bofdir_with_callback( demonID, bofbelt_callback, 'C:\\Windows\\Microsoft.Net\\Framework\\v1.1.4322\\System.dll' )
    bofdir_with_callback( demonID, bofbelt_callback, 'C:\\Windows\\Microsoft.Net\\Framework\\v2.0.50727\\System.dll' )
    bofdir_with_callback( demonID, bofbelt_callback, 'C:\\Windows\\Microsoft.Net\\Framework\\v3.0\\System.dll' )
    bofdir_with_callback( demonID, bofbelt_callback, 'C:\\Windows\\Microsoft.Net\\Framework\\v3.5\\System.dll' )
    bofdir_with_callback( demonID, bofbelt_callback, 'C:\\Windows\\Microsoft.Net\\Framework\\v4.0.30319\\System.dll' )
    reg_query_with_callback( demonID, bofbelt_callback, "HKLM", "SOFTWARE\\Microsoft\\PowerShell\\1\\PowerShellEngine", "PowerShellVersion" )
    reg_query_with_callback( demonID, bofbelt_callback, "HKLM", "SOFTWARE\\Microsoft\\PowerShell\\3\\PowerShellEngine", "PowerShellVersion" )
    reg_query_with_callback( demonID, bofbelt_callback, "HKLM", "SOFTWARE\\Policies\\Microsoft\\Windows\\PowerShell\\Transcription", "EnableTranscripting" )
    reg_query_with_callback( demonID, bofbelt_callback, "HKLM", "SOFTWARE\\Policies\\Microsoft\\Windows\\PowerShell\\Transcription", "EnableInvocationHeader" )
    reg_query_with_callback( demonID, bofbelt_callback, "HKLM", "SOFTWARE\\Policies\\Microsoft\\Windows\\PowerShell\\ModuleLogging", "EnableModuleLogging" )
    reg_query_with_callback( demonID, bofbelt_callback, "HKLM", "SOFTWARE\\Policies\\Microsoft\\Windows\\PowerShell\\ScriptBlockLogging", "EnableScriptBlockLogging" )
    reg_query_with_callback( demonID, bofbelt_callback, "HKLM", "SOFTWARE\\Policies\\Microsoft\\Windows\\PowerShell\\ScriptBlockLogging", "EnableScriptBlockInvocationLogging" )

    # Getting .NET information

    bofdir_with_callback( demonID, bofbelt_callback, 'C:\\Windows\\Microsoft.Net\\Framework\\' )
    reg_query_with_callback( demonID, bofbelt_callback, "HKLM", "SOFTWARE\\Microsoft\\NET Framework Setup\\NDP\\v3.5", "Version" )
    reg_query_with_callback( demonID, bofbelt_callback, "HKLM", "SOFTWARE\\Microsoft\\NET Framework Setup\\NDP\\v4\\Full", "Version" )

    # Getting AVs/EDRs information

    wmi_query_with_callback( demonID, bofbelt_callback, "SELECT * FROM AntiVirusProduct", ".", "root\\SecurityCenter2" )

    # Getting information about the running processes

    tasklist_with_callback( demonID, bofbelt_callback )

    # Getting UAC information

    reg_query_with_callback( demonID, bofbelt_callback, "HKLM", "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System", "ConsentPromptBehaviorAdmin" )
    reg_query_with_callback( demonID, bofbelt_callback, "HKLM", "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System", "EnableLUA" )
    reg_query_with_callback( demonID, bofbelt_callback, "HKLM", "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System", "LocalAccountTokenFilterPolicy" )
    reg_query_with_callback( demonID, bofbelt_callback, "HKLM", "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System", "FilterAdministratorToken" )

    # Getting Local Users information
    userenum_with_callback( demonID, bofbelt_callback )

    # Getting Local Sessions information

    enumlocalsessions_with_callback( demonID, bofbelt_callback )

    # Getting Open windows information

    windowlist_with_callback( demonID, bofbelt_callback )

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, f"Tasked demon to run Bofbelt" )

    return TaskID

RegisterCommand( arp, "", "arp", "Lists out ARP table", 0, "", "" )
RegisterCommand( driversigs, "", "driversigs", "checks drivers for known edr vendor names", 0, "", "" )
RegisterCommand( ipconfig, "", "ipconfig", "Lists out adapters, system hostname and configured dns serve", 0, "", "" )
RegisterCommand( listdns, "", "listdns", "lists dns cache entries", 0, "", "" )
RegisterCommand( locale, "", "locale", "Prints locale information", 0, "", "" )
RegisterCommand( netstat, "", "netstat", "List listening and connected ipv4 udp and tcp connections", 0, "", "" )
RegisterCommand( resources, "", "resources", "list available memory and space on the primary disk drive", 0, "", "" )
RegisterCommand( routeprint, "", "routeprint", "prints ipv4 routes on the machine", 0, "", "" )
RegisterCommand( uptime, "", "uptime", "lists system boot time", 0, "", "" )
RegisterCommand( whoami, "", "whoami", "get the info from whoami /all without starting cmd.exe", 0, "", "" )
RegisterCommand( windowlist, "", "windowlist", "list windows visible on the users desktop", 0, "[opt:all]", "" )
RegisterCommand( reg_query, "", "reg_query", "Query a registry value or enumerate a single key", 0, "[opt:hostname] [hive] [path] [opt: value to query]", "HKLM SYSTEM\\CurrentControlSet\\Control\\Lsa RunAsPPL" )
RegisterCommand( reg_query_recursive, "", "reg_query_recursive", "Recursively enumerate a key starting at path", 0, "[opt:hostname] [hive] [path]", "HKLM SYSTEM\\CurrentControlSet\\Control\\Lsa" )
RegisterCommand( wmi_query, "", "wmi_query", "Run a wmi query and display results in CSV format", 0, "query [opt: server] [opt: namespace]", "\"Select name from Win32_ComputerSystem\"" )
RegisterCommand( nslookup, "", "nslookup", "Make a DNS query. DNS server is the server you want to query (do not specify or 0 for default). Record type is something like A, AAAA, or ANY", 0, "hostname [opt:dns server] [opt: record type]", "dc01" )
RegisterCommand( env, "", "env", "Print environment variables.", 0, "", "" )
RegisterCommand( get_password_policy, "", "get_password_policy", "Gets a server or DC's configured password policy", 0, "[hostname]", "" )
#RegisterCommand( list_firewall_rules, "", "list_firewall_rules", "List Windows firewall rules", 0, "", "" )
RegisterCommand( cacls, "", "cacls", "List user permissions for the specified file, wildcards supported", 0, "[filepath]", "C:\\Windows\\Temp\\test.txt" )
RegisterCommand( schtasksenum, "", "schtasksenum", "Enumerate scheduled tasks on the local or remote computer", 0, "[opt: server]", "" )
RegisterCommand( schtasksquery, "", "schtasksquery", "Query the given task on the local or remote computer", 0, "[opt: server] [taskpath]", "" )
RegisterCommand( sc_enum, "", "sc_enum", "Enumerate services for qc, query, qfailure, and qtriggers info", 0, "[opt: server]", "" )
RegisterCommand( sc_qc, "", "sc_qc", "sc qc impelmentation in BOF", 0, "service_name [opt:server]", "SensorService" )
RegisterCommand( sc_query, "", "sc_query", "sc query implementation in BOF", 0, "[opt: service name] [opt: server]", "" )
RegisterCommand( sc_qdescription, "", "sc_qdescription", "Queries a services description", 0, "service_name [opt: server]", "SensorService" )
RegisterCommand( sc_qfailure, "", "sc_qfailure", "Query a service for failure conditions", 0, "service_name [opt: server]", "SensorService" )
RegisterCommand( sc_qtriggerinfo, "", "sc_qtriggerinfo", "Query a service for trigger conditions", 0, "service_name [opt: server]", "SensorService" )
RegisterCommand( adcs_enum, "", "adcs_enum", "Enumerate CAs and templates in the AD using Win32 functions", 0, "[opt: domain]", "" )
RegisterCommand( enumlocalsessions, "", "enumlocalsessions", "Enumerate currently attached user sessions both local and over RDP", 0, "", "" )
RegisterCommand( enum_filter_driver, "", "enum_filter_driver", "Enumerate filter drivers", 0, "[opt: system]", "" )
RegisterCommand( ldapsearch, "", "ldapsearch", "Execute LDAP searches (NOTE: specify *,ntsecuritydescriptor as attribute parameter if you want all attributes + base64 encoded ACL of the objects, this can then be resolved using BOFHound. Could possibly break pagination, although everything seemed fine during testing.)", 0, "query [opt: attribute] [opt: results_limit] [opt: DC hostname or IP] [opt: Distingished Name]", "\"(&(samAccountType=805306368)(userAccountControl:1.2.840.113556.1.4.803:=4194304))\"" )
RegisterCommand( netsession, "", "get-netsession", "Enumerate sessions on the local or specified computer", 0, "[opt:computer]", "" )
RegisterCommand( netGroupList, "", "netGroupList", "List groups from the default or specified domain", 0, "[opt: domain]", "" )
RegisterCommand( netGroupListMembers, "", "netGroupListMembers", "List group members from the default or specified domain", 0, "groupname [opt: domain]", "" )
RegisterCommand( netLocalGroupList, "", "netLocalGroupList", "List local groups from the local or specified computer", 0, "[opt: server]", "" )
RegisterCommand( netLclGrpLstMmbrs, "", "netLclGrpLstMmbrs", "List local group members from the local or specified group", 0, "groupname [opt: server]", "Administrators" )
RegisterCommand( netuser, "", "netuser", "Get info about specific user. Pull from domain if a domainname is specified", 0, "username [opt: domain]", "Administrator" )
RegisterCommand( userenum, "", "userenum", "Lists user accounts on the current computer", 0, "[opt: <all,locked,disabled,active>]", "" )
RegisterCommand( domainenum, "", "domainenum", "Lists users accounts in the current domain", 0, "[opt: <all,locked,disabled,active>]", "" )
RegisterCommand( netshares, "", "netshares", "List shares on local or remote computer", 0, "<\\\\computername>", "" )
RegisterCommand( netshares, "", "netshares", "List shares on local or remote computer", 0, "[opt: \\\\computername]", "" )
RegisterCommand( netsharesAdmin, "", "netsharesAdmin", "List shares on local or remote computer and gets more info then standard netshares (requires admin)", 0, "[opt: \\\\computername]", "" )
RegisterCommand( netuptime, "", "netuptime", "Returns information about the boot time on the local (or a remote) machine", 0, "[opt: hostname]", "" )
RegisterCommand( netview, "", "netview", "lists local workstations and servers", 0, "[opt: netbios_domain_name]", "" )
RegisterCommand( quser, "", "quser", "Simple implementation of quser.exe usingt the Windows API", 0, "<OPT:TARGET>", "10.10.10.10" )
RegisterCommand( bofdir, "", "bofdir", "Lists a target directory using BOF.", 0, "[directory] [/s]", "C:\\Windows\\Temp" )
RegisterCommand( tasklist, "", "tasklist", "This command displays a list of currently running processes on either a local or remote machine.\nUsage:   tasklist [hostname]\n         hostname    - Optional. Specifies the remote system to connect to. Do\n                        not include or use '.' to indicate the command should\n                        be run on the local system.\nNote:   You must have a valid login token for the system specified if not\n         local. This token can be obtained using make_token.", 0, "[hostname]", "" )
RegisterCommand( bofbelt, "", "bofbelt", "A Seatbelt port using BOFs", 0, "", "" )
