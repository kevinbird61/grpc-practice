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

clean:
	rm -f *.o *.pb.cc *.pb.h grpc_client grpc_server