all:
	@ git submodule update --init --recursive
	@ $(foreach BOF, $(wildcard */), [ -f $(BOF)/makefile ] && [ "$(BOF)" != "Template/" ] && make -C $(BOF) || true ; )
	@ $(foreach BOF, $(wildcard */*/makefile), [ -f $(BOF) ] && make -C $(dir $(BOF)) || true ; )


