SUBDIRS := $(filter-out Template, $(shell echo */))

.PHONY: all $(SUBDIRS)

all: UPDATE $(SUBDIRS)

UPDATE:
	@ echo "Updating submodules"
	@ git submodule update --init --recursive

$(SUBDIRS):
	@ if [ -f $@/makefile -o -f $@/Makefile ]; then \
		echo "Building $@"; \
		$(MAKE) -C $@; \
	else \
		echo "Skipping $@ (Makefile not found)"; \
	fi
