TRANSCRYPT ?= transcrypt
BIND_HOST ?= 127.0.0.1
BIND_PORT ?= 5000
INSTALL_PREFIX ?= install/

.PHONY: all build export testserver buildloop video install

all: build video

video_files ?= public-domain-placeholder.mp4 org_360p.mp4 org_480p.mp4 org_720p.mp4
existing_video_files = $(foreach f,$(video_files),$(shell [ -e ../introvideo/$(f) ] && echo ../introvideo/$(f) ))
video_source = $(firstword $(existing_video_files))
install_files = \
	index.html pixi.js  pixi.js.map  pixi-legacy.js  pixi-legacy.js.map jquery*.js \
	__target__ \
	resources \

video: resources/video/intro.mp4

resources/video/intro.mp4: $(video_source)
	cp $< $@

build:
	$(TRANSCRYPT) -b -m -n -k -o -g main.py

buildloop:
	while true ; do inotifywait -e create -e modify -r . ; make all ; done

testserver:
	FLASK_APP=flask_server:app flask --debug run -h $(BIND_HOST) --port $(BIND_PORT)

install: build video
	mkdir -p $(INSTALL_PREFIX)
	rm -rf $(INSTALL_PREFIX)/*
	cp -r $(install_files) \
		$(INSTALL_PREFIX)/.
