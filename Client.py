import threading
import socket
import _thread
import time
import json

HOST = "127.0.0.1"

def triggered_update(node):
    while 1:
        if node.get_triggered():
            neighbours = node.get_neighbours()
            for id, port in neighbours:
                
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.connect((HOST, port))
                        data = node.get_table()
                        encoded_data = json.dumps(data).encode('utf-8')

                        s.sendall(encoded_data)
                        time.sleep(1)
                        s.close()
                except:
                    pass
            node.reset_triggered()


def find_link_cost(id, table):
    for k,v in table.items():
        if k == id:
            path, link_cost = v
            return link_cost

def update_config(node):
    while 1:
        if node.get_config():
            filename = f'{node.get_id()}config.txt'
            output = f'{len(node.get_neighbours())}\n'
            with open(filename, 'r+') as f:
                neighbours = node.get_neighbours()
                for neighbour in neighbours:
                    id, port = neighbour
                    link_cost = find_link_cost(id, node.get_table())
                    output += f'{id} {link_cost} {port}\n'
                output = output.rstrip('\n')
                f.write(output)
            node.reset_config()

                
            
def routing_calc(node):
    time.sleep(60)  # 60 seconds timeout
    while 1:
        if node.get_updated():
            table = sorted(node.get_table())
            for k in table:
                if k != node.get_id():
                    dest = k
                    path, link_cost = node.get_table()[k]
                    if link_cost != float('inf') or path != 'failed':
                        shortest_path = path + dest
                        print(f"Least cost path from {node.get_id()} to {dest}: {shortest_path}, link cost: {link_cost}")
            node.reset_updated()
            print('\n')

class Client():
    def __init__(self, node):
        self.node = node

    def send_packets_periodically(self):

        while 1:
            time.sleep(10) # 10 seconds delay for broadcasting information value packets

            neighbours = self.node.get_neighbours()
            for id, port in neighbours:
                
                # print(f"Client {self.node.get_id()} is sending packets to {id} server's socket at port {port}...")

                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.connect((HOST, port))
                        # print(f"Client {id}: Connection established with {id} server socket at port {port}")
                        data = self.node.get_table()
                        encoded_data = json.dumps(data).encode('utf-8')

                        s.sendall(encoded_data)
                        time.sleep(1)
                        s.close()
                except:
                    # print(f"Socket {id} at port {port} is not yet established")
                    pass

                # print()

    def send_packets_intially(self):
        i = 0
        neighbours = self.node.get_neighbours()
        while i < len(neighbours):
            id, port = neighbours[i]

            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

                    s.connect((HOST, port))

                    data = self.node.get_table()
                    encoded_data = json.dumps(data).encode('utf-8')

                    s.sendall(encoded_data)
                    i += 1
                    s.close()
            except:
                pass

    def run(self):
       
        try: 
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:#s = socket.socket()         # Create a socket object

                _thread.start_new_thread(routing_calc, (self.node,))
                _thread.start_new_thread(update_config, (self.node,))
                _thread.start_new_thread(triggered_update, (self.node,))

                self.send_packets_intially()
                _thread.start_new_thread(self.send_packets_periodically(), ())    
                 
        except Exception as e:
            print("Client: Can't connect to the Socket")
            print(e)
