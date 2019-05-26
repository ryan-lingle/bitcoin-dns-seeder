from db import *

class Node:
    def __init__(self, id=None, ip=None, port=8333, version=None, services=None, user_agent=None, latest_block=None, relay=None, connection=False, connection_failures=False):
        self.id = id
        self.ip = ip
        self.port = port
        self.version = version
        self.services = services
        self.user_agent = user_agent
        self.latest_block = latest_block
        self.relay = relay
        self.connection = connection
        self.connection_failures = connection_failures

    def __str__(self):
       return self.show()

    def __repr__(self):
       return self.show()

    def show(self):
       return (f'\n{self.__class__.__name__}(\n'
               f'   id={self.id!r},\n'
               f'   ip={self.ip!r},\n'
               f'   port={self.port!r}\n'
               f'   version={self.version!r}\n'
               f'   services={self.services!r}\n'
               f'   user_agent={self.user_agent!r}\n'
               f'   latest_block={self.latest_block!r}\n'
               f'   relay={bool(self.relay)!r}\n'
               f'   connection={bool(self.connection)!r}\n'
               f'   connection_failure={self.connection_failures!r})')



    @property
    def address(self):
        return (self.ip, self.port)

    def update(self, args):
        return update_node(self.id, args)


####################################################
######## NODE CLASS METHODS ########################
####################################################

    @classmethod
    def create(cls, args):
        return create_node(args)

    @classmethod
    def all(cls):
        return all_nodes()

    @classmethod
    def ids(cls):
        print(all_ids())
        return all_ids()

    @classmethod
    def count(cls):
        return node_count()

    @classmethod
    def find_by(cls, args):
        return find_node_by(args)

    @classmethod
    def where(cls, args):
        return nodes_where(args)

    @classmethod
    def connected(cls):
        return nodes_where({ "connection": True })

    @classmethod
    def unconnected(cls, count):
        return unconnected_nodes(count=count)

    def get_relationships():
        return all_relationships()

