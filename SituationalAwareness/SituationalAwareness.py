from havoc import Demon, RegisterCommand
from struct import pack, calcsize

class Packer:
    def __init__(self):
        self.buffer : bytes = b''
        self.size   : int   = 0

    def getbuffer(self):
        return pack("<L", self.size) + self.buffer

    def addshort(self, short):
        self.buffer += pack("<h", short)
        self.size += 2

    def addint(self, dint):
        self.buffer += pack("<i", dint)
        self.size += 4

        print(self.buffer.hex())

    def addstr(self, s):
        s = s.encode("utf-8")
        fmt = "<L{}s".format(len(s) + 1)
        self.buffer += pack(fmt, len(s)+1, s)
        self.size += calcsize(fmt)
        print(f"{self.size} : {self.buffer}")

    def addBytes(self, s, b): 
        fmt = "<L{}s".format(s)
        self.buffer += pack(fmt, s, str(b))
        self.size += calcsize(fmt)

    def addWstr(self, s):
        s = s.encode("utf-16_le")
        fmt = "<L{}s".format(len(s) + 2)
        self.buffer += pack(fmt, len(s)+2, s)
        self.size += calcsize(fmt)


def arp( demonID, *param ):
    TaskID : str    = None
    demon  : Demon  = None

    demon  = Demon( demonID )
    TaskID = demon.ConsoleWrite(demon.CONSOLE_TASK, "Tasked demon to lists out ARP table")

    demon.InlineExecute( TaskID, "go", "ObjectFiles/arp.x64.o", "", False )

    return TaskID

def driversigs( demonID, *param ):
    TaskID : str    = None
    demon  : Demon  = None

    demon  = Demon( demonID )
    TaskID = demon.ConsoleWrite(demon.CONSOLE_TASK, "Tasked demon to check drivers for known edr vendor names")

    demon.InlineExecute( TaskID, "go", "ObjectFiles/driversigs.x64.o", "", False )

    return TaskID

def ipconfig( demonID, *param ):
    TaskID : str    = None
    demon  : Demon  = None

    demon  = Demon( demonID )
    TaskID = demon.ConsoleWrite(demon.CONSOLE_TASK, "Tasked demon to lists out adapters, system hostname and configured dns serve")

    demon.InlineExecute( TaskID, "go", "ObjectFiles/ipconfig.x64.o", "", False )

    return TaskID

def listdns( demonID, *param ):
    TaskID : str    = None
    demon  : Demon  = None

    demon  = Demon( demonID )
    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to lists dns cache entries" )

    demon.InlineExecute( TaskID, "go", "ObjectFiles/listdns.x64.o", "", False )

    return TaskID

def locale( demonID, *param ):
    TaskID : str    = None
    demon  : Demon  = None

    demon  = Demon( demonID )
    TaskID = demon.ConsoleWrite(demon.CONSOLE_TASK, "Tasked demon to retrieve system locale information, date format, and country")

    demon.InlineExecute( TaskID, "go", "ObjectFiles/locale.x64.o", "", False )

    return TaskID

def netstat( demonID, *param ):
    TaskID : str    = None
    demon  : Demon  = None

    demon  = Demon( demonID )
    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to get local ipv4 udp/tcp listening and connected ports" )

    demon.InlineExecute( TaskID, "go", "ObjectFiles/netstat.x64.o", "", False )

    return TaskID

def resources( demonID, *param ):
    TaskID : str    = None
    demon  : Demon  = None

    demon  = Demon( demonID )
    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to list available memory and space on the primary disk drive" )

    demon.InlineExecute( TaskID, "go", "ObjectFiles/resources.x64.o", "", False )

    return TaskID

def routeprint( demonID, *param ):
    TaskID : str    = None
    demon  : Demon  = None

    demon  = Demon( demonID )
    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to prints ipv4 routes on the machine" )

    demon.InlineExecute( TaskID, "go", "ObjectFiles/routeprint.x64.o", "", False )

    return TaskID

def uptime( demonID, *param ):
    TaskID : str    = None
    demon  : Demon  = None

    demon  = Demon( demonID )
    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to lists system boot time" )

    demon.InlineExecute( TaskID, "go", "ObjectFiles/uptime.x64.o", "", False )

    return TaskID

def whoami( demonID, *param ):
    TaskID : str    = None
    demon  : Demon  = None

    demon  = Demon( demonID )
    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to get the info from whoami /all without starting cmd.exe" )

    demon.InlineExecute( TaskID, "go", "ObjectFiles/whoami.x64.o", "", False )

    return TaskID

def windowlist( demonID, *param ):
    TaskID : str    = None
    demon  : Demon  = None

    demon  = Demon( demonID )
    TaskID = demon.ConsoleWrite( demon.CONSOLE_TASK, "Tasked demon to list windows visible on the users desktop" )

    demon.InlineExecute( TaskID, "go", "ObjectFiles/windowlist.x64.o", "", False )

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
RegisterCommand( windowlist, "", "windowlist", "list windows visible on the users desktop", 0, "", "" )
