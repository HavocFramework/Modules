BOFNAME := dir
COMINCLUDE := -I src/
CC_x64 := x86_64-w64-mingw32-gcc
CC_x86 := i686-w64-mingw32-gcc
CC=x86_64-w64-mingw32-clang

all:
	$(CC_x64) -o bin/$(BOFNAME).x64.o $(COMINCLUDE) -c src/timestomp.c

clean:
	rm -f /bin/$(BOFNAME).*

