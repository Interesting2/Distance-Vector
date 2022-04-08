import time

class Node():
    def __init__(self, id, port):
        self.id = id
        self.port = port
        self.neighbours = []
        self.table = {}     # routing table
        self.updated = False    # check whether we can output the least cost path to the terminal
        self.config = False     # check whether we can update the config files
        self.counter = 0        # checks when the network is converged
        self.timer = {}         # timer to detect if neighbour nodes are alive
        self.triggered = False  # triggered update when link cost changes
        self.reachability = {}

        # reachability matrix

        # dictionary of dictionaries
        # Each inner dictionary is a routing table of a neighbour node or itself
        # Key of inner dictionaries is Destination node id
        # Value of inner dictionaries is the tuple of (least cost path, link_cost)

        """
        {
           'A': {'A': ('', 0),
                'B': ('', 1.0),
                'C': (2, 1.0)},
            },
            'B': {'B': ('', 0)
                'A': ('', 1.0),
                'C': ('', 1.0)},
            },
            'C': {'C': ('', 0),
                'B': ('', 1.0),
                'A': ('', 1.0)}
            }
        }
        """
        

    def __str__(self):
        return f"Id is: {self.id}\nPort is: {self.port}\nNeighbours are: {self.neighbours}\nTable is: {self.table}\n"

    def in_reach(self, id):
        return id in self.reachability

    def get_reachability(self, id):
        return self.reachability[id]

    def add_reach_table(self, id, packets):
        self.reachability[id] = packets

    def get_triggered(self):
        return self.triggered
    
    def reset_triggered(self):
        self.triggered = False

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