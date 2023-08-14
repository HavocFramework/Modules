#
# Beacon Object File ( BOF ) Compiler
# 
# Used to create object files that are
# compatible with Beacon's inline-execute
# command.
#

CC_x64 := x86_64-w64-mingw32-gcc
LD_x64 := x86_64-w64-mingw32-ld
STRx64 := x86_64-w64-mingw32-strip
CC_x86 := i686-w64-mingw32-gcc
LD_x86 := i686-w64-mingw32-ld
STRx86 := i686-w64-mingw32-strip

SOURCE := $(wildcard source/*.c)
OBJECT := $(SOURCE:%.c=%.o)
CFLAGS := -Os -s -Qn -nostdlib 
LFLAGS := -Wl,-s,--exclude-all-symbols

all: $(OBJECT)
	$(LD_x64) -x -r source/*_x64.o -o regdump.x64.o
	$(LD_x86) -x -r source/*_x86.o -o regdump.x86.o

.c.o:
	$(CC_x64) -o $(basename $@)_x64.o -c $< $(CFLAGS) $(LFLAGS)
	$(STRx64) -N $(basename $(notdir $@)).c $(basename $@)_x64.o
	$(CC_x86) -o $(basename $@)_x86.o -c $< $(CFLAGS) $(LFLAGS)
	$(STRx86) -N $(basename $(notdir $@)).c $(basename $@)_x86.o

clean:
	rm -rf source/*_x64.o
	rm -rf source/*_x86.o
	rm -rf regdump.x64.o regdump.x86.o
