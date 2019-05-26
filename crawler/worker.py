from threading import Thread
from connection_service import ConnectionService
from utils import BitcoinProtocolError
from node import Node

class Worker(Thread):
    def __init__(self, unconnected_node_queue, timeout, n):
        super().__init__()
        self.unconnected_node_queue = unconnected_node_queue
        self.timeout = timeout
        self.n = n

    def run(self):
        while True:
            print(f"starting thread {self.n}")
            node = self.unconnected_node_queue.get()

            try:
                conn = None
                conn = ConnectionService(node, timeout=self.timeout)
                conn.open()
            except (OSError, BitcoinProtocolError) as e:
                print(f'Got error: {str(e)}')
                if node.connection_failures:
                    node.update({"connection_failures": node.connection_failures + 1})
                else:
                    node.update({"connection_failures": 1})
            finally:
                if conn:
                    conn.close()
                    print(f'Discovered {len(conn.nodes_discovered)} peers from {conn.node.ip}')
