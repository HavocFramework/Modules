/**
 * KaynLdr
 * Author: Paul Ungur (@C5pider)
 */

#include <KaynLdr.h>
#include <stdio.h>
#include <InvokeAssembly.h>

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

    Instance.Modules.Mscoree = LoadLibraryA( "Mscoree" );
    if ( Instance.Modules.Msvcrt )
    {
        Instance.Win32.CLRCreateInstance = GetProcAddress( Instance.Modules.Mscoree, "CLRCreateInstance" );
    }
}

VOID ModuleMain( PVOID Params )
{
    PARSER Parser = { 0 };
    ParserNew( &Parser, Params );

    InvokeAssembly( &Parser );
}