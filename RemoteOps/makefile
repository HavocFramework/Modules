NAME = CS-Remote-OPs-BOF
BIN  = bin

all:
	@ cd $(NAME); chmod +x make_all.sh; bash ./make_all.sh
	@ find $(NAME)/Injection -name '*.o' -exec cp {} $(BIN)/ \;
	@ find $(NAME)/Remote -name '*.o' -exec cp {} $(BIN)/ \;

clean:
	rm $(BIN)/*.o
