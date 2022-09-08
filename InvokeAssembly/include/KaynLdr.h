/**
 * KaynLdr
 * Author: Paul Ungur (@C5pider)
 */

#ifndef KAYNLDR_KAYNLDR_H
#define KAYNLDR_KAYNLDR_H

#define _NO_NTDLL_CRT_

#include <windows.h>
#include <Native.h>

#define DLL_QUERY_HMODULE   6

#define HASH_KEY 5381

#ifdef _WIN64
#define PPEB_PTR __readgsqword( 0x60 )
#else
#define PPEB_PTR __readgsqword( 0x30 )
#endif

#define MemCopy                         __builtin_memcpy
#define NTDLL_HASH                      0x70e61753

#define SYS_LDRLOADDLL                  0x9e456a43
#define SYS_NTALLOCATEVIRTUALMEMORY     0xf783b8ec
#define SYS_NTPROTECTEDVIRTUALMEMORY    0x50e92888

#define DLLEXPORT                       __declspec( dllexport )
#define WIN32_FUNC( x )                 __typeof__( x ) * x;

#define U_PTR( x )                      ( ( UINT_PTR ) x )
#define C_PTR( x )                      ( ( LPVOID ) x )

typedef struct {

    struct {
        WIN32_FUNC( LdrLoadDll );
        WIN32_FUNC( NtAllocateVirtualMemory )
        WIN32_FUNC( NtProtectVirtualMemory )
    } Win32;

    struct {
        PVOID   Ntdll;
    } Modules ;

} KAYNINSTANCE, *PKAYNINSTANCE ;

LPVOID  KaynCaller();

typedef struct {
    WORD offset :12;
    WORD type   :4;
} *PIMAGE_RELOC;

PVOID   KGetModuleByHash( DWORD hash );
PVOID   KGetProcAddressByHash( PKAYNINSTANCE Instance, PVOID DllModuleBase, DWORD FunctionHash, DWORD Ordinal );
PVOID   KLoadLibrary( PKAYNINSTANCE Instance, LPSTR Module );

VOID    KResolveIAT( PKAYNINSTANCE Instance, PVOID KaynImage, PVOID IatDir );
VOID    KReAllocSections( PVOID KaynImage, PVOID ImageBase, PVOID Dir );

DWORD   KHashString( LPVOID String, SIZE_T Size );
SIZE_T  KStringLengthA( LPCSTR String );
SIZE_T  KStringLengthW( LPCWSTR String );
VOID    KMemSet( PVOID Destination, INT Value, SIZE_T Size );
SIZE_T  KCharStringToWCharString( PWCHAR Destination, PCHAR Source, SIZE_T MaximumAllowed );

#endif
