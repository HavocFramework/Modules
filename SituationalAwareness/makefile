NAME 			= CS-Situational-Awareness-BOF
BIN			= ObjectFiles

all:
	@cd $(NAME); chmod +x make_all.sh; bash ./make_all.sh
	@find $(NAME)/SA -name '*.o' -exec cp {} $(BIN)/ \;

clean:
	rm $(BIN)/*.o
