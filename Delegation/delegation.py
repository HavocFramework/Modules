from havoc import Demon, RegisterCommand, RegisterModule
import re

def get_delegation( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = Packer()
    demon  = Demon( demonID )

    del_query = {
        'constrained': '(&(objectCategory=computer)(userAccountControl:1.2.840.113556.1.4.803:=16777216))',
        'unconstrained': '(&(objectClass=computer)(primarygroupid=515)(userAccountControl:1.2.840.113556.1.4.803:=524288))',
        'rbcd': '(&(msDS-AllowedToActOnBehalfOfOtherIdentity=*)(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))'
    }

    del_attrs = {
        'constrained': 'sAMAccountName,msDS-AllowedToDelegateTo',
        'unconstrained': 'sAMAccountName',
        'rbcd': 'sAMAccountName'
    }

    num_params = len(params)
    query = ''
    attributes = ''
    result_limit = 0
    hostname = ''
    domain = ''

    if num_params < 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Not enough parameters" )
        return False

    if num_params > 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return False

    if params[ 0 ].lower() not in del_query:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Wrong first parameter" )
        return False

    query = del_query[ params[ 0 ].lower() ]
    attrs = del_attrs[ params[ 0 ].lower() ]

    if num_params >= 2:
        attributes = params[ 1 ]

    # not used
    if num_params >= 3:
        result_limit = params[ 2 ]

    if num_params >= 4:
        hostname = params[ 3 ]

    if num_params >= 5:
        domain = params[ 4 ]

    packer.addstr(query)
    packer.addstr(attrs)
    packer.adduint32(result_limit)
    packer.addstr(hostname)
    packer.addstr(domain)

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to run ldap query" )

    demon.InlineExecute( TaskID, "go", f"bin/ldapsearch.{demon.ProcessArch}.o", packer.getbuffer(), False )

    return TaskID

def get_spns( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = Packer()
    demon  = Demon( demonID )

    num_params = len(params)
    query = '(&(samAccountType=805306368)(!samAccountName=krbtgt)(serviceprincipalname=*)(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))'
    attributes = 'sAMAccountName,servicePrincipalName'
    result_limit = 0
    hostname = ''
    domain = ''

    if num_params > 0:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return False

    # not used
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


def get_asrep( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = Packer()
    demon  = Demon( demonID )

    num_params = len(params)
    query = '(&(userAccountControl:1.2.840.113556.1.4.803:=4194304)(!(UserAccountControl:1.2.840.113556.1.4.803:=2)))'
    attributes = 'sAMAccountName'
    result_limit = 0
    hostname = ''
    domain = ''

    if num_params > 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return False

    # not used
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


RegisterCommand( get_delegation, "", "get-delegation", "Enumerate a given domain for different types of abusable Kerberos Delegation settings.", 0, "[Constrained,Unconstrained,RBCD]", "constrained" )
RegisterCommand( get_spns, "", "get-spns", "Enumerate a given domain for user accounts with SPNs.", 0, "", "" )
RegisterCommand( get_asrep, "", "get-asrep", "Enumerate a given domain for user accounts with ASREP.", 0, "", "" )
