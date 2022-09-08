/**
 * KaynLdr
 * Author: Paul Ungur (@C5pider)
 */

#include <KaynLdr.h>
#include <DModule.h>
#include <Parser.h>
#include <stdio.h>

HINSTANCE   hAppInstance = NULL;
INSTANCE    Instance     = { 0 };

BOOL WINAPI DllMain( HINSTANCE hInstDLL, DWORD dwReason, LPVOID lpReserved )
{
    BOOL bReturnValue = TRUE;

    switch( dwReason )
    {
        case DLL_QUERY_HMODULE:
            if( lpReserved != NULL )
                *( HMODULE* ) lpReserved = hAppInstance;
            break;

		case DLL_PROCESS_ATTACH:
		{
			hAppInstance = hInstDLL;

            ModuleInit();
            ModuleMain( lpReserved );

			fflush( stdout );
			ExitProcess( 0 );
		}

        case DLL_PROCESS_DETACH:
        case DLL_THREAD_ATTACH:
        case DLL_THREAD_DETACH:
            break;
    }
    return bReturnValue;
}

VOID ModuleInit()
{
    Instance.Modules.Msvcrt = LoadLibraryA( "Msvcrt" );
    if ( Instance.Modules.Msvcrt )
    {
        Instance.Win32.printf = GetProcAddress( Instance.Modules.Msvcrt, "printf" );
    }
}

VOID ModuleMain( PVOID Params )
{
    PARSER  Parser = { 0 };
    PCHAR   Test   = NULL;
    UINT32  Size   = 0;

    ParserNew( &Parser, Params );

    Test = ParserGetBytes( &Parser, &Size );

    Instance.Win32.printf( "Test [%d]: %s\n", Size, Test );

    Instance.Win32.printf( "[+] Hello from KaynLdr Module\n" );
    Instance.Win32.printf( "[*] Process ID: %d\n", GetCurrentProcessId());
}