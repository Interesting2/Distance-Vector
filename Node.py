import time

class Node():
    def __init__(self, id, port):
        self.id = id
        self.port = port
        self.neighbours = []

        # reachability matrix
        # Key is Destination node id
        # Value is the tuple of (least cost path, link_cost)
        self.table = {}
        self.updated = False
        self.config = False
        self.received = {}
        self.counter = 0
        self.timer = {}

    def __str__(self):
        return f"Id is: {self.id}\nPort is: {self.port}\nNeighbours are: {self.neighbours}\nTable is: {self.table}\n"

    def add_node_timer(self, id):
        self.timer[id] = time.time()
    
    def get_node_timer(self, id):
        return self.timer[id]
        
    def add_neighbour(self, id, port):
        self.neighbours.append((id, port))

    def get_neighbours(self):
        return self.neighbours
    
    def get_received(self):
        return self.received
    
    def add_received(self, id):
        self.received.append(id)

    def get_id(self):
        return self.id

    def get_port(self):
        return self.port

    def init_table(self, table):
        self.table = table
                
    def get_updated(self):
        return self.updated

    def reset_updated(self):
        self.updated = False

    def get_table(self):
        return self.table

    def get_config(self):
        return self.config

    def reset_config(self):
        self.config = False