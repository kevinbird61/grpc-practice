CXX = g++
CPPFLAGS += `pkg-config --cflags protobuf grpc`
CXXFLAGS += -std=c++11

LDFLAGS += -L/usr/local/lib `pkg-config --libs protobuf grpc++ grpc`\
           -Wl,--no-as-needed -lgrpc++_reflection -Wl,--as-needed\
           -ldl

PROTOC = protoc
GRPC_CPP_PLUGIN = grpc_cpp_plugin 
GRPC_CPP_PLUGIN_PATH ?= `which $(GRPC_CPP_PLUGIN)`

# define protos location
PROTOS_PATH = ../protos/

# doc config
DOCS_LAYOUT = jasonm23-dark

vpath %.proto $(PROTOS_PATH)

all: grpc_client grpc_server

grpc_client: helloworld.pb.o helloworld.grpc.pb.o grpc_client.o
	$(CXX) $^ $(LDFLAGS) -o $@

grpc_server: helloworld.pb.o helloworld.grpc.pb.o grpc_server.o
	$(CXX) $^ $(LDFLAGS) -o $@

.PRECIOUS: %.grpc.pb.cc
%.grpc.pb.cc: %.proto
	$(PROTOC) -I $(PROTOS_PATH) --grpc_out=. --plugin=protoc-gen-grpc=$(GRPC_CPP_PLUGIN_PATH) $<

.PRECIOUS: %.pb.cc
%.pb.cc: %.proto
	$(PROTOC) -I $(PROTOS_PATH) --cpp_out=. $<

# Making doc (Static Html) from markdown-styles
# Please make sure you have been install nodejs
doc_page:
	# install doc generator
	cd ../doc/ && npm install 
	# 01-HelloWorld
	../doc/node_modules/markdown-styles/bin/generate-md \
		--layout $(DOCS_LAYOUT) \
		--input ../doc/01-HelloWorld \
		--output ../doc/01-HelloWorld

clean:
	rm -f *.o *.pb.cc *.pb.h grpc_client grpc_server

clean_doc:
	rm -rf ../doc/01-HelloWorld/assets
	rm -f ../doc/01-HelloWorld/*.html