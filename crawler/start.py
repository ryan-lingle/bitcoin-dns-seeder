import socket
from db import create_tables
from node import Node
from connection_service import ConnectionService
from crawler import Crawler


DNS_SEEDS = [
    'dnsseed.bitcoin.dashjr.org',
    'dnsseed.bluematt.me',
    'seed.bitcoin.sipa.be',
    'seed.bitcoinstats.com',
    'seed.bitcoin.jonasschnelli.ch',
    'seed.btc.petertodd.org',
    'seed.bitcoin.sprovoost.nl',
    'dnsseed.emzy.de',
]


def query_dns_seeds():
    nodes = []
    for seed in DNS_SEEDS:
        try:
            addr_info = socket.getaddrinfo(seed, 8333, 0, socket.SOCK_STREAM)
            addresses = [ai[-1][:2] for ai in addr_info]
            for addr in addresses:
                Node.create({"ip": addr[0], "port": addr[1]})
        except OSError as e:
            print(f"DNS seed query failed: {str(e)}")

if __name__ == '__main__':
    create_tables()
    # local_node = Node.create({ "ip": "localhost", "port": 8333 })
    # print(local_node)
    count = Node.count()
    print(f"Database at Node Count: {count}")

    # local_connection = ConnectionService(local_node, timeout=15)
    # local_connection.open()
    if int(count) < 50:
        query_dns_seeds()
        print(f"Received {int(Node.count()) - count} nodes from core dev dns seed.")
    print("Starting Crawler")
    Crawler(num_workers=10).crawl()
