from havoc import Demon, RegisterCommand, RegisterModule
import re

class DelegationPacker:
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

def get_delegation( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = DelegationPacker()
    demon  = Demon( demonID )

    del_query = {
        'constrained': '(&(userAccountControl:1.2.840.113556.1.4.803:=524288)(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))',
        'constrainedproto': '(&(userAccountControl:1.2.840.113556.1.4.803:=16777216)(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))',
        'unconstrained': '(&(msDS-AllowedToDelegateTo=*)(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))',
        'rbcd': '(&(msDS-AllowedToActOnBehalfOfOtherIdentity=*)(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))'
    }

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

    if params[ 0 ].lower() not in del_query:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Wrong first parameter" )
        return True

    query = del_query[ params[ 0 ].lower() ]

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

    demon.InlineExecute( TaskID, "go", f"bin/ldapsearch.{demon.ProcessArch}.o", packer.getbuffer(), False )

    return TaskID

def get_spns( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = DelegationPacker()
    demon  = Demon( demonID )

    spn_query = {
        'spn': '(&(samAccountType=805306368)(!samAccountName=krbtgt)(serviceprincipalname=*)(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))',
        'asrep': '(&(userAccountControl:1.2.840.113556.1.4.803 : = 4194304)(!(UserAccountControl:1.2.840.113556.1.4.803 : = 2)))'
    }

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

    if params[ 0 ].lower() not in spn_query:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Wrong first parameter" )
        return True

    query = spn_query[ params[ 0 ] ]

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

    demon.InlineExecute( TaskID, "go", f"bin/ldapsearch.{demon.ProcessArch}.o", packer.getbuffer(), False )

    return TaskID

RegisterCommand( get_delegation, "", "get-delegation", "Enumerate a given domain for different types of abusable Kerberos Delegation settings.", 0, "[Constrained,ConstrainedProto,Unconstrained,RBCD] [opt: attribute] [opt: results_limit] [opt: DC hostname or IP] [opt: Distingished Name]", "constrained" )
RegisterCommand( get_spns, "", "get-spns", "Enumerate a given domain for user accounts with SPNs and ASREP.", 0, "[spn,ASREP] [opt: attribute] [opt: results_limit] [opt: DC hostname or IP] [opt: Distingished Name]", "spn" )
