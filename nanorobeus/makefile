BOFNAME := nanorobeus
CC_x64 := x86_64-w64-mingw32-gcc
CC_x86 := i686-w64-mingw32-gcc
STRIP := strip
OPTIONS := -O3 -masm=intel -Wall -Wextra -g -I include -fno-reorder-functions

.PHONY: all

all: bof_64 bof_86

bof_64:
	$(CC_x64) -c src/entry.c -o bin/$(BOFNAME).x64.o -DBOF $(OPTIONS)
	$(STRIP) --strip-unneeded bin/$(BOFNAME).x64.o

bof_86:
	$(CC_x86) -c src/entry.c -o bin/$(BOFNAME).x86.o -DBOF $(OPTIONS)
	$(STRIP) --strip-unneeded bin/$(BOFNAME).x86.o
