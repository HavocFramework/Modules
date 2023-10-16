from havoc import Demon, RegisterCommand

def testdll(demonID, *param):
    TaskID : str    = None
    demon  : Demon  = None
    packer = Packer()

    packer.addstr("test1234")

    demon  = Demon(demonID)
    TaskID = demon.ConsoleWrite(demon.CONSOLE_TASK, "Tasked demon spawn and inject a test dll")
    
    arg = packer.getbuffer() 

    demon.DllSpawn(TaskID, "/tmp/test.dll", arg)

    return TaskID

RegisterCommand(testdll, "", "testdll", "spawn and inject test dll", 0, "", "")
