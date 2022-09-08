
#include <windows.h>
#include <KaynLdr.h>
#include <stdio.h>

typedef struct _INSTANCE {

    struct {

        WIN32_FUNC( printf )
        WINBASEAPI HRESULT ( WINAPI *CLRCreateInstance ) ( REFCLSID clsid, REFIID riid, LPVOID* ppInterface );

    } Win32;

    struct {

        PVOID Msvcrt;
        PVOID Mscoree;

    } Modules;

} INSTANCE, *PINSTANCE;

extern INSTANCE Instance;

VOID ModuleInit();
VOID ModuleMain();