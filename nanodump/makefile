NAME 			= nanodump
BIN			= bin

all:
	@ cd $(NAME); make -f Makefile.mingw
	@ find $(NAME)/dist -name '*.o' -exec cp {} $(BIN)/ \;

clean:
	rm $(BIN)/*.o
