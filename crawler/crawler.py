from queue import Queue
from worker import Worker
from node import Node
import sys


class Crawler:
    def __init__(self, num_workers=10, timeout=10):
        self.timeout = timeout
        self.unconnected_node_queue = Queue()
        self.workers = [ Worker(self.unconnected_node_queue, self.timeout, i) for i in range(num_workers)
        ]
    def add_nodes(self):
        for node in Node.unconnected(len(self.workers) * 10):
            self.unconnected_node_queue.put(node)

    def main_loop(self):
        # ensure unconnectd node queue stays larger than num_workers
        while True:
            # Fill input queue if running low
            if self.unconnected_node_queue.qsize() < len(self.workers):
                self.add_nodes()

            # print a report to the console
            # print(f"{len(Node.connected())} nodes connected. {Node.count()} total.")

    def crawl(self):
        # fill worker inputs queue
        self.add_nodes()

        # start workers
        for worker in self.workers:
            worker.start()

        # start main loop
        self.main_loop()
