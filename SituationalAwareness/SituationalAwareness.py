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

def arp( demonID, *param ):
    TaskID : str    = None
    demon  : Demon  = None

    demon  = Demon( demonID )
    TaskID = demon.ConsoleWrite(demon.CONSOLE_TASK, "Tasked demon to lists out ARP table")

    demon.InlineExecute( TaskID, "go", "ObjectFiles/arp.x64.o", b'', False )

    return TaskID

def driversigs( demonID, *param ):
    TaskID : str    = None
    demon  : Demon  = None

    demon  = Demon( demonID )
    TaskID = demon.ConsoleWrite(demon.CONSOLE_TASK, "Tasked demon to check drivers for known edr vendor names")

    demon.InlineExecute( TaskID, "go", "ObjectFiles/driversigs.x64.o", b'', False )

    return TaskID

def ipconfig( demonID, *param ):
    TaskID : str    = None
    demon  : Demon  = None

    demon  = Demon( demonID )
    TaskID = demon.ConsoleWrite(demon.CONSOLE_TASK, "Tasked demon to lists out adapters, system hostname and configured dns serve")

    demon.InlineExecute( TaskID, "go", "ObjectFiles/ipconfig.x64.o", b'', False )

    return TaskID

def listdns( demonID, *param ):
    TaskID : str    = None
    demon  : Demon  = None

    demon  = Demon( demonID )
    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to lists dns cache entries" )

    demon.InlineExecute( TaskID, "go", "ObjectFiles/listdns.x64.o", b'', False )

    return TaskID

def locale( demonID, *param ):
    TaskID : str    = None
    demon  : Demon  = None

    demon  = Demon( demonID )
    TaskID = demon.ConsoleWrite(demon.CONSOLE_TASK, "Tasked demon to retrieve system locale information, date format, and country")

    demon.InlineExecute( TaskID, "go", "ObjectFiles/locale.x64.o", b'', False )

    return TaskID

def netstat( demonID, *param ):
    TaskID : str    = None
    demon  : Demon  = None

    demon  = Demon( demonID )
    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to get local ipv4 udp/tcp listening and connected ports" )

    demon.InlineExecute( TaskID, "go", "ObjectFiles/netstat.x64.o", b'', False )

    return TaskID

def resources( demonID, *param ):
    TaskID : str    = None
    demon  : Demon  = None

    demon  = Demon( demonID )
    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to list available memory and space on the primary disk drive" )

    demon.InlineExecute( TaskID, "go", "ObjectFiles/resources.x64.o", b'', False )

    return TaskID

def routeprint( demonID, *param ):
    TaskID : str    = None
    demon  : Demon  = None

    demon  = Demon( demonID )
    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to prints ipv4 routes on the machine" )

    demon.InlineExecute( TaskID, "go", "ObjectFiles/routeprint.x64.o", b'', False )

    return TaskID

def uptime( demonID, *param ):
    TaskID : str    = None
    demon  : Demon  = None

    demon  = Demon( demonID )
    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to lists system boot time" )

    demon.InlineExecute( TaskID, "go", "ObjectFiles/uptime.x64.o", b'', False )

    return TaskID

def whoami( demonID, *param ):
    TaskID : str    = None
    demon  : Demon  = None

    demon  = Demon( demonID )
    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to get the info from whoami /all without starting cmd.exe" )

    demon.InlineExecute( TaskID, "go", "ObjectFiles/whoami.x64.o", b'', False )

    return TaskID

def windowlist( demonID, *param ):
    TaskID : str    = None
    demon  : Demon  = None

    demon  = Demon( demonID )
    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to list windows visible on the users desktop" )

    demon.InlineExecute( TaskID, "go", "ObjectFiles/windowlist.x64.o", b'', False )

    return TaskID

def reg_query( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = MyPacker()
    demon  = Demon( demonID )

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
        return True

    if num_params > 4:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return True

    if params[ params_parsed ].upper() not in reghives:
        hostname = params[ params_parsed ]
        params_parsed += 1
    else:
        hostname = None

    if params[ params_parsed ].upper() not in reghives:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Provided registry hive value is invalid" )
        return True

    hive = reghives[ params[ params_parsed ].upper() ]
    params_parsed += 1

    if num_params < params_parsed + 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Missing parameters" )
        return True

    path = params[ params_parsed ]
    params_parsed += 1

    if num_params > params_parsed:
        key = params[ params_parsed ]
    else:
        key = None

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to query the windows registry" )

    packer.addstr(hostname)
    packer.adduint32(hive)
    packer.addstr(path)
    packer.addstr(key)
    packer.addbool(False) # recursive

    demon.InlineExecute( TaskID, "go", "ObjectFiles/reg_query.x64.o", packer.getbuffer(), False )

    return TaskID

def reg_query_recursive( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = MyPacker()
    demon  = Demon( demonID )

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
        return True

    if num_params > 3:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return True

    if params[ params_parsed ].upper() not in reghives:
        hostname = params[ params_parsed ]
        params_parsed += 1
    else:
        hostname = None

    if params[ params_parsed ].upper() not in reghives:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Provided registry hive value is invalid" )
        return True

    hive = reghives[ params[ params_parsed ].upper() ]
    params_parsed += 1

    if num_params < params_parsed + 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Missing parameters" )
        return True

    path = params[ params_parsed ]

    key = None

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to query the windows registry recursively" )

    packer.addstr(hostname)
    packer.adduint32(hive)
    packer.addstr(path)
    packer.addstr(key)
    packer.addbool(True) # recursive

    demon.InlineExecute( TaskID, "go", "ObjectFiles/reg_query.x64.o", packer.getbuffer(), False )

    return TaskID

def wmi_query( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = MyPacker()
    demon  = Demon( demonID )

    query     = ''
    server    = '.'
    namespace = 'root\\cimv2'

    params = ' '.join(params)

    # parse parameters that contain quotes
    params = re.findall(r'".+?"|[^ ]+', params)
    params = [param.strip('"') for param in params]
    num_params = len(params)

    if num_params < 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Missing parameters" )
        return True

    if num_params > 3:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return True

    query = params[ 0 ]

    if num_params > 1:
        server = params[ 1 ]

    if num_params > 2:
        namespace = params[ 2 ]

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to query the Windows Management Toolkit" )

    packer.addWstr(server)
    packer.addWstr(namespace)
    packer.addWstr(query)

    demon.InlineExecute( TaskID, "go", "ObjectFiles/wmi_query.x64.o", packer.getbuffer(), False )

    return TaskID

def nslookup( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = MyPacker()
    demon  = Demon( demonID )

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
        return True

    lookup = params[ 0 ]

    if num_params > 1:
        server = params[ 1 ]
        if server == '127.0.0.1':
            demon.ConsoleWrite( demon.CONSOLE_ERROR, "Localhost dns query's have a potential to crash, refusing" )
            return True

    if num_params > 2 and params[ 2 ].upper() in recordmapping:
        _type = recordmapping[ params[ 2 ].upper() ]

    if num_params > 3:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return True

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to run DNS query" )

    packer.addstr(lookup)
    packer.addstr(server)
    packer.addshort(_type)

    demon.InlineExecute( TaskID, "go", "ObjectFiles/nslookup.x64.o", packer.getbuffer(), False )

    return TaskID

def env( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    demon  = Demon( demonID )

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to obtain the environment variables for the current process" )

    demon.InlineExecute( TaskID, "go", "ObjectFiles/env.x64.o", b'', False )

    return TaskID

def get_password_policy( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = MyPacker()
    demon  = Demon( demonID )

    num_params = len(params)
    hostname = '.'

    if num_params == 1:
        hostname = params[ 0 ]

    if num_params > 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return True

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to obtain the password policy" )

    packer.addWstr(hostname)

    demon.InlineExecute( TaskID, "go", "ObjectFiles/get_password_policy.x64.o", packer.getbuffer(), False )

    return TaskID

def list_firewall_rules( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = MyPacker()
    demon  = Demon( demonID )

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to list all firewall rules" )

    demon.InlineExecute( TaskID, "go", "ObjectFiles/get_password_policy.x64.o", b'', False )

    return TaskID

def cacls( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = MyPacker()
    demon  = Demon( demonID )

    num_params = len(params)

    if num_params < 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Not enough parameters" )
        return True

    filepath = params[ 0 ]

    if num_params > 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return True

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to obtain file permissions" )

    packer.addWstr(filepath)

    demon.InlineExecute( TaskID, "go", "ObjectFiles/cacls.x64.o", packer.getbuffer(), False )

    return TaskID

def schtasksenum( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = MyPacker()
    demon  = Demon( demonID )

    num_params = len(params)
    server = ''

    if num_params == 1:
        server = params[ 0 ]

    if num_params > 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return True

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to list all scheduled tasks" )

    packer.addWstr(server)

    demon.InlineExecute( TaskID, "go", "ObjectFiles/schtasksenum.x64.o", packer.getbuffer(), False )

    return TaskID

def schtasksquery( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = MyPacker()
    demon  = Demon( demonID )

    num_params = len(params)
    service = ''
    server = ''

    if num_params == 0:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Not enough parameters" )
        return True

    if num_params == 1:
        service = params[ 0 ]
    elif num_params == 2:
        server = params[ 0 ]
        service = params[ 1 ]
    else:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return True

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to query a given scheduled task" )

    packer.addWstr(server)
    packer.addWstr(service)

    demon.InlineExecute( TaskID, "go", "ObjectFiles/schtasksquery.x64.o", packer.getbuffer(), False )

    return TaskID

def sc_enum( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = MyPacker()
    demon  = Demon( demonID )

    num_params = len(params)
    server = ''

    if num_params == 1:
        server = params[ 0 ]

    if num_params > 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return True

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to enumerate all service configs" )

    packer.addstr(server)

    demon.InlineExecute( TaskID, "go", "ObjectFiles/sc_enum.x64.o", packer.getbuffer(), False )

    return TaskID

def sc_qc( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = MyPacker()
    demon  = Demon( demonID )

    num_params = len(params)
    service = ''
    server = ''

    if num_params == 0:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Not enough parameters" )
        return True

    if num_params == 1:
        service = params[ 0 ]
    elif num_params == 2:
        service = params[ 0 ]
        server = params[ 1 ]
    else:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return True

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to run sc qc" )

    packer.addstr(server)
    packer.addstr(service)

    demon.InlineExecute( TaskID, "go", "ObjectFiles/sc_qc.x64.o", packer.getbuffer(), False )

    return TaskID

def sc_query( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = MyPacker()
    demon  = Demon( demonID )

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
        return True

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to run sc query" )

    packer.addstr(server)
    packer.addstr(service)

    demon.InlineExecute( TaskID, "go", "ObjectFiles/sc_query.x64.o", packer.getbuffer(), False )

    return TaskID

def sc_qdescription( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = MyPacker()
    demon  = Demon( demonID )

    num_params = len(params)
    service = ''
    server = ''

    if num_params == 0:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Not enough parameters" )
        return True

    if num_params == 1:
        service = params[ 0 ]
    elif num_params == 2:
        service = params[ 0 ]
        server = params[ 1 ]
    else:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return True

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to get the description of a service" )

    packer.addstr(server)
    packer.addstr(service)

    demon.InlineExecute( TaskID, "go", "ObjectFiles/sc_qdescription.x64.o", packer.getbuffer(), False )

    return TaskID

def sc_qfailure( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = MyPacker()
    demon  = Demon( demonID )

    num_params = len(params)
    service = ''
    server = ''

    if num_params == 0:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Not enough parameters" )
        return True

    if num_params == 1:
        service = params[ 0 ]
    elif num_params == 2:
        service = params[ 0 ]
        server = params[ 1 ]
    else:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return True

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to get the failure reason for a service" )

    packer.addstr(server)
    packer.addstr(service)

    demon.InlineExecute( TaskID, "go", "ObjectFiles/sc_qfailure.x64.o", packer.getbuffer(), False )

    return TaskID

def sc_qtriggerinfo( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = MyPacker()
    demon  = Demon( demonID )

    num_params = len(params)
    service = ''
    server = ''

    if num_params == 0:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Not enough parameters" )
        return True

    if num_params == 1:
        service = params[ 0 ]
    elif num_params == 2:
        service = params[ 0 ]
        server = params[ 1 ]
    else:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return True

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to get the failure reason for a service" )

    packer.addstr(server)
    packer.addstr(service)

    demon.InlineExecute( TaskID, "go", "ObjectFiles/sc_qtriggerinfo.x64.o", packer.getbuffer(), False )

    return TaskID

def adcs_enum( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = MyPacker()
    demon  = Demon( demonID )

    num_params = len(params)
    domain = ''

    if num_params > 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return True

    if num_params == 1:
        domain = params[ 0 ]

    packer.addWstr(domain)

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to enumerate CAs and templates in the AD" )

    demon.InlineExecute( TaskID, "go", "ObjectFiles/adcs_enum.x64.o", packer.getbuffer(), False )

    return TaskID

def enumlocalsessions( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = MyPacker()
    demon  = Demon( demonID )

    num_params = len(params)

    if num_params > 0:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return True

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to enumerate currently attached user sessions both local and over RDP" )

    demon.InlineExecute( TaskID, "go", "ObjectFiles/enumlocalsessions.x64.o", b'', False )

    return TaskID

def enum_filter_driver( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = MyPacker()
    demon  = Demon( demonID )

    num_params = len(params)
    system = ''

    if num_params > 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return True

    if num_params == 1:
        system = params[ 0 ]

    packer.addstr(system)

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to enumerate filter drivers" )

    demon.InlineExecute( TaskID, "go", "ObjectFiles/enum_filter_driver.x64.o", packer.getbuffer(), False )

    return TaskID

def ldapsearch( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = MyPacker()
    demon  = Demon( demonID )

    # parse parameters that contain quotes
    params = re.findall(r'".+?"|[^ ]+', params)
    params = [param.strip('"') for param in params]
    num_params = len(params)

    query = ''
    attributes = ''
    result_limit = 0
    hostname = ''
    domain = ''

    if num_params < 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Not enough parameters" )
        return True

    if num_params > 5:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return True

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

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to run ldap query" )

    demon.InlineExecute( TaskID, "go", "ObjectFiles/ldapsearch.x64.o", packer.getbuffer(), False )

    return TaskID

def netsession( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = MyPacker()
    demon  = Demon( demonID )

    num_params = len(params)
    computer = ''

    if num_params == 1:
        computer = params[ 0 ]
    elif num_params > 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return True

    packer.addWstr(computer)

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to enumerate sessions on the local or specified computer" )

    demon.InlineExecute( TaskID, "go", "ObjectFiles/get-netsession.x64.o", packer.getbuffer(), False )

    return TaskID

def netGroupList( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = MyPacker()
    demon  = Demon( demonID )

    num_params = len(params)
    domain = ''
    group = ''

    if num_params == 1:
        domain = params[ 0 ]
    elif num_params > 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return True

    packer.addshort(0)
    packer.addWstr(domain)
    packer.addWstr(group)

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to list groups from the default or specified domain" )

    demon.InlineExecute( TaskID, "go", "ObjectFiles/netgroup.x64.o", packer.getbuffer(), False )

    return TaskID

def netGroupListMembers( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = MyPacker()
    demon  = Demon( demonID )

    num_params = len(params)
    domain = ''
    group = ''

    if num_params < 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Not enough parameters" )
        return True
    elif num_params == 1:
        group = params[ 0 ]
    elif num_params == 2:
        domain = params[ 1 ]
    else:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return True

    packer.addshort(1)
    packer.addWstr(domain)
    packer.addWstr(group)

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to list group members from the default or specified domain" )

    demon.InlineExecute( TaskID, "go", "ObjectFiles/netgroup.x64.o", packer.getbuffer(), False )

    return TaskID

def netLocalGroupList( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = MyPacker()
    demon  = Demon( demonID )

    num_params = len(params)
    server = ''
    group = ''

    if num_params == 1:
        server = params[ 0 ]
    elif num_params > 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return True

    packer.addshort(0)
    packer.addWstr(server)
    packer.addWstr(group)

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to list local groups from the local or specified computer" )

    demon.InlineExecute( TaskID, "go", "ObjectFiles/netlocalgroup.x64.o", packer.getbuffer(), False )

    return TaskID

def netGroupListMembers( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = MyPacker()
    demon  = Demon( demonID )

    num_params = len(params)
    domain = ''
    group = ''

    if num_params < 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Not enough parameters" )
        return True
    elif num_params == 1:
        group = params[ 0 ]
    elif num_params == 2:
        domain = params[ 1 ]
    else:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return True

    packer.addshort(1)
    packer.addWstr(domain)
    packer.addWstr(group)

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to list local group members" )

    demon.InlineExecute( TaskID, "go", "ObjectFiles/netlocalgroup.x64.o", packer.getbuffer(), False )

    return TaskID

def netLocalGroupListMembers( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = MyPacker()
    demon  = Demon( demonID )

    num_params = len(params)
    domain = ''
    group = ''

    if num_params < 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Not enough parameters" )
        return True
    elif num_params == 1:
        group = params[ 0 ]
    elif num_params == 2:
        group = params[ 0 ]
        domain = params[ 1 ]
    else:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return True

    packer.addshort(1)
    packer.addWstr(domain)
    packer.addWstr(group)

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to list local group members" )

    demon.InlineExecute( TaskID, "go", "ObjectFiles/netlocalgroup.x64.o", packer.getbuffer(), False )

    return TaskID

def netuser( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = MyPacker()
    demon  = Demon( demonID )

    num_params = len(params)
    username = ''
    domain = ''

    if num_params < 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Not enough parameters" )
        return True
    elif num_params == 1:
        username = params[ 0 ]
    elif num_params == 2:
        username = params[ 0 ]
        domain = params[ 1 ]
    else:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return True

    packer.addWstr(username)
    packer.addWstr(domain)

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to get info about specific user" )

    demon.InlineExecute( TaskID, "go", "ObjectFiles/netuser.x64.o", packer.getbuffer(), False )

    return TaskID

def userenum( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = MyPacker()
    demon  = Demon( demonID )

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
            return True
        _type = enumtype[ params[ 0 ].lower() ]
    elif num_params > 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return True

    packer.adduint32(0)
    packer.adduint32(_type)

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to list user accounts on the current computer" )

    demon.InlineExecute( TaskID, "go", "ObjectFiles/netuserenum.x64.o", packer.getbuffer(), False )

    return TaskID

def domainenum( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = MyPacker()
    demon  = Demon( demonID )

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
            return True
        _type = enumtype[ params[ 0 ].lower() ]
    elif num_params > 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return True

    packer.adduint32(1)
    packer.adduint32(_type)

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to list user accounts in the current domain" )

    demon.InlineExecute( TaskID, "go", "ObjectFiles/netuserenum.x64.o", packer.getbuffer(), False )

    return TaskID

def netshares( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = MyPacker()
    demon  = Demon( demonID )

    num_params = len(params)
    computer = ''

    if num_params == 1:
        computer = params[ 0 ]
    elif num_params > 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return True

    packer.addWstr(computer)
    packer.adduint32(0)

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to list shares on local or remote computer" )

    demon.InlineExecute( TaskID, "go", "ObjectFiles/netshares.x64.o", packer.getbuffer(), False )

    return TaskID

def netsharesAdmin( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = MyPacker()
    demon  = Demon( demonID )

    num_params = len(params)
    computer = ''

    if num_params == 1:
        computer = params[ 0 ]
    elif num_params > 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return True

    packer.addWstr(computer)
    packer.adduint32(1)

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to list shares on local or remote computer" )

    demon.InlineExecute( TaskID, "go", "ObjectFiles/netshares.x64.o", packer.getbuffer(), False )

    return TaskID

def netuptime( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = MyPacker()
    demon  = Demon( demonID )

    num_params = len(params)
    hostname = ''

    if num_params == 1:
        hostname = params[ 0 ]
    elif num_params > 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return True

    packer.addWstr(hostname)

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to list local workstations and servers" )

    demon.InlineExecute( TaskID, "go", "ObjectFiles/netuptime.x64.o", packer.getbuffer(), False )

    return TaskID

def netview( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = MyPacker()
    demon  = Demon( demonID )

    num_params = len(params)
    computer = ''

    if num_params == 1:
        computer = params[ 0 ]
    elif num_params > 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return True

    packer.addWstr(computer)

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to list local workstations and servers" )

    demon.InlineExecute( TaskID, "go", "ObjectFiles/netview.x64.o", packer.getbuffer(), False )

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
RegisterCommand( netLocalGroupListMembers, "", "netLocalGroupListMembers", "List local group members from the local or specified group", 0, "groupname [opt: server]", "Administrators" )
RegisterCommand( netuser, "", "netuser", "Get info about specific user. Pull from domain if a domainname is specified", 0, "username [opt: domain]", "Administrator" )
RegisterCommand( userenum, "", "userenum", "Lists user accounts on the current computer", 0, "[opt: <all,locked,disabled,active>]", "" )
RegisterCommand( domainenum, "", "domainenum", "Lists users accounts in the current domain", 0, "[opt: <all,locked,disabled,active>]", "" )
RegisterCommand( netshares, "", "netshares", "List shares on local or remote computer", 0, "<\\\\computername>", "" )
RegisterCommand( netshares, "", "netshares", "List shares on local or remote computer", 0, "[opt: \\\\computername]", "" )
RegisterCommand( netsharesAdmin, "", "netsharesAdmin", "List shares on local or remote computer and gets more info then standard netshares (requires admin)", 0, "[opt: \\\\computername]", "" )
RegisterCommand( netuptime, "", "netuptime", "Returns information about the boot time on the local (or a remote) machine", 0, "[opt: hostname]", "" )
RegisterCommand( netview, "", "netview", "lists local workstations and servers", 0, "[opt: netbios_domain_name]", "" )
