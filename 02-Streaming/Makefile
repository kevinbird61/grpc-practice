all: protos/route_guide.proto
	python -m grpc_tools.protoc -I./protos --python_out=. --grpc_python_out=. ./protos/route_guide.proto
