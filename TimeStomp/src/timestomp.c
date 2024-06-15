//Author: robot
//Date: 20231212
//This C++ File timestomps a supplied target file based off the create, modify, and last access time of a source file as a BOF
//Intended use timestomp.o go <target file> <source file>

#include <windows.h>
#include "beacon.h"

//Required API imports
WINBASEAPI WINBOOL WINAPI KERNEL32$SetFileTime (HANDLE fhandle, LPFILETIME attribute1, LPFILETIME attribute2, LPFILETIME attribute3);
WINBASEAPI WINBOOL WINAPI KERNEL32$GetFileTime (HANDLE fhandle, LPFILETIME attribute1, LPFILETIME attribute2, LPFILETIME attribute3);
WINBASEAPI HANDLE WINAPI KERNEL32$CreateFileA (LPCSTR val1, DWORD val2, DWORD val3, LPSECURITY_ATTRIBUTES val4, DWORD val5, DWORD val6, HANDLE fhandle);
WINBASEAPI WINBOOL WINAPI KERNEL32$CloseHandle (HANDLE fhandle);
WINBASEAPI DWORD WINAPI KERNEL32$GetLastError (VOID);

//Main BOF method
void go(char * args, int len) {
    datap parser;
    HANDLE targetHandle, sourceHandle;
    FILETIME creationTime, lastAccessTime, lastWriteTime;

    //Parse Args
    BeaconDataParse(&parser, args, len);
    char* fileString1 = BeaconDataExtract(&parser, NULL);
    char* fileString2 = BeaconDataExtract(&parser, NULL);

    if (fileString1 == NULL || fileString2 == NULL) {
        BeaconPrintf(CALLBACK_OUTPUT, "[!] Error processing supplied file names. Ensure you supply the target file and then the source file.\n");
        return;
    }

    //get a handle to the target file
    targetHandle = KERNEL32$CreateFileA(fileString1,
        FILE_WRITE_ATTRIBUTES, 0,
        NULL, OPEN_EXISTING,
        FILE_ATTRIBUTE_NORMAL, NULL);

    if (targetHandle == INVALID_HANDLE_VALUE) {
        BeaconPrintf(CALLBACK_OUTPUT, "[!] Could not obtain handle to target file. Error 0x%1x\n", KERNEL32$GetLastError());
        return;
    }

    //get a handle to the source file
    sourceHandle = KERNEL32$CreateFileA(fileString2,
        FILE_READ_ATTRIBUTES, FILE_SHARE_READ,
        NULL, OPEN_EXISTING,
        FILE_ATTRIBUTE_NORMAL, NULL);

    if (sourceHandle == INVALID_HANDLE_VALUE) {
        BeaconPrintf(CALLBACK_OUTPUT, "[!] Could not obtain handle to source file. Error 0x%1x\n", KERNEL32$GetLastError());
        return;
    }

    //Get the source file times
    if (! KERNEL32$GetFileTime(sourceHandle, &creationTime, &lastAccessTime, &lastWriteTime)) {
        BeaconPrintf(CALLBACK_OUTPUT, "[!] Error getting file times. Error code: 0x%1x\n", KERNEL32$GetLastError());
        KERNEL32$CloseHandle(sourceHandle);
        KERNEL32$CloseHandle(targetHandle);
        return;
    }

    //set the filetime on the target file
    if (! KERNEL32$SetFileTime(targetHandle, &creationTime, &lastAccessTime, &lastWriteTime)) {
        BeaconPrintf(CALLBACK_OUTPUT, "[!] Setting the filetime failed. Error code: 0x%1x\n", KERNEL32$GetLastError());
        KERNEL32$CloseHandle(sourceHandle);
        KERNEL32$CloseHandle(targetHandle);
        return;
    }

    BeaconPrintf(CALLBACK_OUTPUT, "++Time-stomped++\n"); //inform user of success

    //close our handles.
    KERNEL32$CloseHandle(targetHandle);
    KERNEL32$CloseHandle(sourceHandle);

    return;
}
