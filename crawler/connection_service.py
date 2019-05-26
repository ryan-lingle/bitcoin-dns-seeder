import socket
from node import Node
from utils import handshake, read_msg, serialize_msg, read_addr_payload
version_attrs = ('version', 'services', 'user_agent', 'latest_block', 'relay')

class ConnectionService:
    def __init__(self, node, timeout):
        self.node = node
        self.sock = socket.create_connection(node.address, timeout=timeout)
        self.stream = None
        self.nodes_discovered = []

    def remain_alive(self):
        return not self.nodes_discovered

    def handle_msg(self):
        message = read_msg(self.stream)
        command = message["command"]
        payload = message["payload"]
        print(f'Received a "{command}" of {len(payload)} bytes')
        if command == b'ping':
            res = serialize_msg(command=b'pong', payload=payload)
            self.sock.sendall(res)
            print("Send 'pong'")
        elif command == b'addr':
            self.nodes_discovered = [ Node.create({"ip":address["ip"], "port": address["port"]}) for address in payload["addresses"] ]

    def open(self):
        print(f'Connecting to {self.node.ip}')

        version_msg = handshake(self.sock)
        while version_msg["command"] != b"version":
            version_msg = handshake(self.sock)

        version_extract = dict((k, version_msg["payload"][k]) for k in version_attrs)
        version_extract["connection"] = True
        print(self.node.update(version_extract))
        self.stream = self.sock.makefile('rb')

        print(f'Sending "getaddr" to {self.node.ip}')
        msg = serialize_msg(command=b"getaddr")
        self.sock.sendall(msg)

        # Handle messages until program exists
        while self.remain_alive():
            self.handle_msg()

    def close(self):
        # Clean up socket's file descriptor
        if self.sock:
            self.sock.close()
