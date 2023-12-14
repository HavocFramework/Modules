NAME 			= No-Consolation
BIN			= bin

all:
	@ cd $(NAME); make
	@ find $(NAME)/dist -name '*.o' -exec cp {} $(BIN)/ \;

clean:
	rm $(BIN)/*.o
