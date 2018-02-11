# for document
PROTO=../protos/README.md

all: protos
	npm install 
	# using papogen
	node_modules/papogen/main.js \
		-s . \
		-g md -m md_doc \
		-o . -t Learning-gRPC

protos: 
	cp $(PROTO) 00\ Protobuf.md