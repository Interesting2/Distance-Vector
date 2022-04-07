import threading
import socket
import _thread
import time
import json

HOST = "127.0.0.1"

def update_neighbour(node):
    neighbours = node.get_neighbours()
    for id, port in neighbours:
        
        # print(f"Client {self.node.get_id()} is sending packets to {id} server's socket at port {port}...")
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((HOST, port))
                # print(f"Client {id}: Connection established with {id} server socket at port {port}")
                data = node.get_table()
                encoded_data = json.dumps(data).encode('utf-8')

                s.sendall(encoded_data)
                time.sleep(1)
                s.close()
        except:
            # print(f"Socket {id} at port {port} is not yet established")
            pass


def find_link_cost(id, table):
    for k,v in table.items():
        if k == id:
            path, link_cost = v
            return link_cost

def update_config(node):
    while 1:
        if node.get_config():
            # print(f"I am Node {node.get_id()} updating the configuration file...")
            filename = f'{node.get_id()}config.txt'
            output = f'{len(node.get_neighbours())}\n'
            with open(filename, 'r+') as f:
                neighbours = node.get_neighbours()
                for neighbour in neighbours:
                    id, port = neighbour
                    link_cost = find_link_cost(id, node.get_table())
                    output += f'{id} {link_cost} {port}\n'
                output = output.rstrip('\n')
                print(f"New Content of the config file for {filename}")
                print(output)
                f.write(output)
            node.reset_config()
            update_neighbour(node)      # once link cost changed, config file updated, then update the neighbour

                
            
def routing_calc(node):
    time.sleep(60)  # 60 seconds timeout
    print("60 seconds passed: Routing calculation waiting to for link cost change...")
    while 1:
        if node.get_updated():
            # print(f"I am Node {node.get_id()}")
            table = sorted(node.get_table())
            for k in table:
                if k != node.get_id():
                    # print(f"{k} : {v}")
                    dest = k
                    path, link_cost = node.get_table()[k]
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
            print("10 Seconds passed, start sending packets")

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
            # print(f"Client {self.node.get_id()} is sending packets to {id} server's socket at port {port}")
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    # print(f"Connecting to port {port}...")
                    s.connect((HOST, port))
                    # print(f"Client {self.node.get_id()}: Connection established with {id} server socket at port {port}")
                    # print(self.node)
                    # time.sleep(2)
                    data = self.node.get_table()
                    encoded_data = json.dumps(data).encode('utf-8')

                    s.sendall(encoded_data)
                    # delay before closing connection to other server socket
                    # time.sleep(1)
                    # print("WOKE UP")
                    i += 1
                    s.close()
            except:
                pass
                # print(f"Socket {id} at port {port} is not yet established")

            # print()
            # time.sleep(2)
        print("Send Packets Intially Ended...")

    def run(self):
       
        try: 
            print("Client.py")
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:#s = socket.socket()         # Create a socket object

                _thread.start_new_thread(routing_calc, (self.node,))
                # _thread.start_new_thread(update_config, (self.node,))
                # s.connect((HOST, self.node.get_port()))
                # print(f"Client {self.node.get_id()} connected with server socket...")

                self.send_packets_intially()
                _thread.start_new_thread(self.send_packets_periodically(), ())    
                 
               
                # print("Client: Start while loop...\n")

                # while(1):
                    # Start new thread for sending packets periodically to neighbour nodes
                    # print("Periodically updating...")
                    # time.sleep(10)

                    
                    # print(f"Client: Number of active threads: {threading.active_count()}")
                    # print(f"Client {self.node.get_id()} Updated...")
                    


                #     print(f"Client {self.id} woke up...")
                #     mess = self.id + ": Hello, what time is it?"
                #     mess_data = bytes(mess, encoding= 'utf-8')
                #     s.sendall(mess_data)
                #     s.settimeout(2)
                    # data_rev = s.recv(1024)
                    # decoded_data = data_rec.decode('utf-8')
                    # if decoded_data == 'Closed':
                    #     break
                #     if not data_rev:
                #         print("didn't get data")
                #         break
                    
                # s.close()   
        except Exception as e:
            print("Client: Can't connect to the Socket")
            print(e)
