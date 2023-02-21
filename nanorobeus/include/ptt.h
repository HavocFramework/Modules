#pragma once

#include <windows.h>
#include "common.h"
#include "base64.h"

#define _KerbSubmitTicketMessage 21

typedef struct _KERB_CRYPTO_KEY32
{
    int KeyType;
    int Length;
    int Offset;
} KERB_CRYPTO_KEY32, *PKERB_CRYPTO_KEY32;

typedef struct _KERB_SUBMIT_TKT_REQUEST
{
    KERB_PROTOCOL_MESSAGE_TYPE MessageType;
    LUID LogonId;
    int Flags;
    KERB_CRYPTO_KEY32 Key; // key to decrypt KERB_CRED
    int KerbCredSize;
    int KerbCredOffset;
} KERB_SUBMIT_TKT_REQUEST, *PKERB_SUBMIT_TKT_REQUEST;

void execute_ptt(WCHAR** dispatch, HANDLE hToken, char* ticket, LUID luid, BOOL currentLuid);