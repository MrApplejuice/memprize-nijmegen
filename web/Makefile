TRANSCRYPT ?= transcrypt

.PHONY: all build export

all: build export

build:
	$(TRANSCRYPT) -b -m -n -k -o -g main.py

export:
	mkdir -p export
	cp -r index.html pixi* jquery* resources __target__  export/.
