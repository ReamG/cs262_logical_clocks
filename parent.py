import grpc
import threading
import consts
from concurrent import futures
from parent_wire import schema_pb2 as schema, schema_pb2_grpc as services

class ParentServicer(object):
    """
    Parent class for our simulation processes
    """
    def __init__(self):
        """
        Initialize the service handler
        """
        self.children: list[schema.Identity] = []
        self.child_lock: threading.Lock = threading.Lock()

    def ImAlive(self, request, context) -> schema.BirthResponse:
        """
        Handle the creation of a new child process to enter the model
        """
        with self.child_lock:
            if len(self.children) >= consts.MAX_CLIENTS:
                return schema.BirthResponse(success=False, error_message="Too many children")
            new_name = str(len(self.children))
            new_port = 50052 + len(self.children)
            new_identity: schema.Identity = schema.Identity(name=new_name, port=new_port)
            peers = self.children
            self.children.append(new_identity)
        print(f"New child: {new_identity.name} on port {new_identity.port}")
        return schema.BirthResponse(success=True, error_message="", identity=new_identity, peers=peers)
    
    def ImDying(self, request: schema.Identity, _) -> schema.DeathResponse:
        """
        Handle the death of a child process
        """
        with self.child_lock:
            self.children.remove(request)
        print(f"Child {request.name} on port {request.port} has died")
        return schema.DeathResponse()

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    services.add_ParentServicer_to_server(ParentServicer(), server)
    server.add_insecure_port(f"[::]:{consts.PARENT_PORT}")
    server.start()
    server.wait_for_termination()

if __name__ == "__main__":
    serve()