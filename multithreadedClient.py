#!/usr/bin/env python
"""
Multi-threaded TCP Client

multithreadedClient.py is a TCP client that maintains a maximum number of worker threads which continuously send a given
number of requests to multithreadedServer.py and print the server's response.

This is derived from an assignment for the Distributed Systems class at Bennington College
"""
import json
import sys
import os
from ctypes import *
from queue import Queue
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
import textwrap
from socket import SO_REUSEADDR, SOCK_STREAM, error, socket, SOL_SOCKET, AF_INET
from threading import Thread

#--------------------------------------#
########## CLIENT CONSTRUCTOR ##########
#--------------------------------------#


class Client:
    def __init__(self, id, address, port, message):
        self.s = socket(AF_INET, SOCK_STREAM)
        self.id = id
        self.address = address
        self.port = port
        # buf = bytes()
        # for i in range(args.size): # args.size cycles of 1024 bytes messages
        #     v = (c_byte * (1024))(1 % 0x111111111) #1024 bytes
        #     buf += bytearray(v)   
        # self.message = bytes(self.message, 'utf-8')
        # self.message = buf #str(message)

    def run(self):
        try:
            # Timeout if the no connection can be made in 5 seconds
            self.s.settimeout(5)
            # Allow socket address reuse
            self.s.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
            # Connect to the ip over the given port
            self.s.connect((self.address, self.port))
            # Notify that the connection has been established
            print( self.id, ":  connected to ", self.address, " over port", self.port)  
            self.message = json.dumps("Hello World").encode()           
            # Notify that the message is being sent
            print( self.id, ":  sent: ", self.message)        
            # Send the defined request message
            self.s.send(self.message)                      
            while True:
                # Wait to receive data back from server
                data = self.s.recv(1024)
                # Notify that data has been received
                print( self.id, ":  received: ", data)
                # If the data received is not empty, print it   
                if data:
                    if "Username" in data.decode('utf-8'):
                        self.message = json.dumps("user").encode()
                        print( self.id, ":  sent: ", self.message)
                    elif "Password" in data.decode('utf-8'):
                        self.message = json.dumps("pass").encode()    
                    elif "Hello World" in data.decode('utf-8'):
                        self.message = json.dumps("Hello World").encode()          
                        print( self.id, ":  sent: ", self.message)     
                        break  
                    self.s.send(self.message)                                                              
            # CLOSE THE SOCKET
            self.s.close()
        # If something went wrong, notify the user
        # except error as e:
        #     print( "\nERROR: Could not connect to ", self.address, " over port", self.port, "\n")
        except error as e:
            print(f"Error during data exchange: {e}")   
            # raise e
            exit(1)

#------------------------------------------------#
########## DEFINE QUEUE WORKER FUNCTION ##########
#------------------------------------------------#

# Create a queue to hold the tasks for the worker threads
q = Queue(maxsize=0)


# Function which generates a Client instance, getting the work item to be processed from the queue
def worker():
    message = "HELO"

    while True:
        # Get the task from teh work queue
        item = q.get()

        new_client = Client(item, args.ip, args.port, message)
        new_client.run()
        # Mark this task item done, thus removing it from the work queue
        q.task_done()


def main():
    
    if args.version :
        print( "switch_disturber.py v%s" % (__version__, ) )
        sys.exit(0)

    #--------------------------------------------------#
    ########## INITIATE CLIENT WORKER THREADS ##########
    #--------------------------------------------------#

    # Populate the work queue with a list of numbers as long as the total number of requests wished to be sent.
    # These queue items can be thought of as decrementing counters for the client thread workers.
    for item in range(args.requests):
        q.put(item)

    # Create a number of threads, given by the maxWorkerThread variable, to initiate clients and begin sending requests.
    for i in range(args.threads):
        t = Thread(target=worker)
        t.daemon = True
        t.start()

    # Do not exit the main thread until the sub-threads complete their work queue
    q.join()

if __name__ == '__main__':
    try:
        description = """\
            This script can be used to generate high traffic to load the switch.
            It sends messages as byte array to the specified IP and port via socket in multiple threads.
            For more information please take a look in the 'optional arguments' description
            below. 
            """
        example_of_use = """ 
                Set the IP and port: python switch_disturber.py -i 192.168.1.50 -p 60001
            """
        parser = ArgumentParser \
            ( formatter_class=ArgumentDefaultsHelpFormatter
            , description = textwrap.dedent (description)
            , epilog = textwrap.dedent (example_of_use)
            )

        parser.add_argument \
                ( "-v", "--version"
                , action = "store_true"
                , help = "show program's version number and exit"
                )

        parser.add_argument \
                ( "-i", "--ip"
                , type=str
                , default="127.0.0.1"
                , help = "IP of the destination"        
                )

        parser.add_argument \
                ( "-p", "--port"
                , type=int
                , default=12345
                , help = "port of the destination"
                )

        parser.add_argument \
                ( "-s", "--size"
                , type=int
                , default=10
                , help = "message's size in kb"
                )

        parser.add_argument \
                ( "-t", "--threads"
                , type=int
                , default=1
                , help = "number of threads"
                )
        parser.add_argument('-r', '--requests', default=1, type=int, help='Total number of requests to send to server')                
        
        args = parser.parse_args () # parse the command line
        main()
    except KeyboardInterrupt:
        print ('Script interrupted')
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0) 