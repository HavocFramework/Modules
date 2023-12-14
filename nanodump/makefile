NAME 			= nanodump
BIN			= bin

all:
	@ make -C $(NAME) -f Makefile.mingw
	@ find $(NAME)/dist -name '*.o' -exec cp {} $(BIN)/ \;

clean:
	rm $(BIN)/*.o
