TRANSCRYPT ?= transcrypt
BIND_HOST ?= 127.0.0.1
BIND_PORT ?= 5000

.PHONY: all build export testserver

all: build export

build:
	$(TRANSCRYPT) -b -m -n -k -o -g main.py

export:
	mkdir -p export
	cp -r index.html pixi* jquery* resources __target__  export/.

testserver:
	FLASK_APP=flask_server:app flask --debug run -h $(BIND_HOST) --port $(BIND_PORT)
