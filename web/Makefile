TRANSCRYPT ?= transcrypt
BIND_HOST ?= 127.0.0.1
BIND_PORT ?= 5000

.PHONY: all build export testserver buildloop

all: build export

build:
	$(TRANSCRYPT) -b -m -n -k -o -g main.py

export:
	mkdir -p export
	cp -r index.html pixi* jquery* resources __target__  export/.

buildloop:
	while true ; do inotifywait -e create -e modify -r . ; make all ; done

testserver:
	FLASK_APP=flask_server:app flask --debug run -h $(BIND_HOST) --port $(BIND_PORT)
