
#include <windows.h>

typedef struct {
    PCHAR   original;
    PCHAR   buffer;
    UINT32  length;
} PARSER, *PPARSER ;

VOID    ParserNew( PPARSER parser, PCHAR buffer );
INT     ParserGetInt32( PPARSER parser);
PCHAR   ParserGetBytes( PPARSER parser, PINT size);