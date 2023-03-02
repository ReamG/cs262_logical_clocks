freeze:
    pip3 freeze > requirements.txt

generate_grpc:
    python3 -m grpc_tools.protoc -I=. --python_out=. --pyi_out=. --grpc_python_out=. ./parent_wire/schema.proto

.SILENT:
start_parent:
    python3 -u parent.py > parent.out & echo $$! > parent.pid

.SILENT:
stop_parent:
    kill `cat parent.pid`
