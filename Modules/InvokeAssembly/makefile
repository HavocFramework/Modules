MAKEFLAGS 		+= -s

NAME 			= InvokeAssembly

COMPILER_x86 	= i686-w64-mingw32-gcc
COMPILER_x64 	= x86_64-w64-mingw32-gcc

CFLAGS			=  -Os -fno-asynchronous-unwind-tables -shared -masm=intel
CFLAGS 			+= -fno-ident -fpack-struct=8 -falign-functions=1
CFLAGS  		+= -s -ffunction-sections -falign-jumps=1 -w
CFLAGS			+= -falign-labels=1 -fPIC
CFLAGS			+= -Wl,-s,--no-seh,--enable-stdcall-fixup
CFLAGS			+= -l oleaut32 -l uuid

INCLUDE			= -I include
SOURCE 			= $(wildcard src/*.c)

x64:
	nasm -f win64 src/Util.s -o src/Util.o
	$(COMPILER_x64) src/*.o $(INCLUDE) $(SOURCE) $(CFLAGS) -o bin/$(NAME).x64.dll -lntdll -luser32
	rm src/*.o