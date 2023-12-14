SUBDIRS := $(wildcard */)

.PHONY: all $(SUBDIRS)

all: $(SUBDIRS)

$(SUBDIRS):
	@if [ -f $@/makefile ]; then \
		echo "Building $@"; \
		$(MAKE) -C $@; \
	else \
		echo "Skipping $@ (makefile not found)"; \
	fi
