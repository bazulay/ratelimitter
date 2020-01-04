#!/bin/bash

python -m grpc_tools.protoc --proto_path=. ./ratelimitter.proto --python_out=. --grpc_python_out=.
