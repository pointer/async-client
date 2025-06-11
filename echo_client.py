# -*- coding: utf-8 -*-
__version__ = "1.0.0"
__doc__     = """High traffic generator to load switch for the switch demonstration"""


import asyncio
import threading
from ctypes import *
from faker import Faker
import socket
import argparse
import textwrap
import json
import sys
import os
from ctypes import *
from queue import Queue
import asyncio
import time
from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
import textwrap
from socket import SO_REUSEADDR, SOCK_STREAM, error, socket, SOL_SOCKET, AF_INET
from threading import Thread
from signal import signal, SIGPIPE, SIG_DFL
from socket import socket, AF_INET, SOCK_STREAM, error
from socket import create_connection
from socket import SOL_SOCKET, SO_REUSEADDR
from socket import timeout as socket_timeout
from socket import timeout as socket_timeout
from socket import error as socket_error

signal(SIGPIPE,SIG_DFL)
#// ln -s /...libboostSourceFiles.../libboost_thread.so /..RequestTOmtFiles.../libboost_thread-mt.so
args = None
lock = threading.Lock()


HOST = '127.0.0.1'  # Server address
PORT = 12345        # Server port

# Credentials for authentication
default_username = 'user'
default_password = 'pass'
q = Queue(maxsize=0)

def print_help():
    print("""
Available commands:
  <text>           Echo text to server
  QUIT             Close the session
  LIST_SESSIONS    Print session info to server console
  HELP             Show this help message
""")

#--------------------------------------#
########## CLIENT CONSTRUCTOR ##########
#--------------------------------------#

class Client:
        # def __init__(self, host, port, path, headers, method):
        # self.host = host.decode('utf-8')
        # self.hostname = socket.gethostbyname(self.host)
        # self.port = port
        # self.path = path.decode('utf-8')
        # self.header = headers
        # self.method = method.decode('utf-8')
        # self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    def __init__(self, id, address, port, message):
        # self.sock = socket(AF_INET, SOCK_STREAM)
        self.sock = None
        self.id = id
        self.address = address
        self.port = port
        self.fake = Faker()
        self.my_word_list = [
            'danish','cheesecake','sugar',
            'Lollipop','wafer','Gummies',
            'sesame','Jelly','beans',
            'pie','bar','Ice','oat' ]
        self.register_endpoint = "REGISTER"
        self.login_endpoint = "/LOGIN"
        self.delete_account_endpoint = "/delete_account"      
        self.users= dict  
        # buf = bytes()
        # for i in range(args.size): # args.size cycles of 1024 bytes messages
        #     v = (c_byte * (1024))(1 % 0x111111111) #1024 bytes
        #     buf += bytearray(v)   
        # self.message = bytes(self.message, 'utf-8')
        # self.message = buf #str(message)


    def register(self, username, password, email):
        registration_data = { "email": email, "username": username, "password": password}
        response = requests.post(self.base_url + self.register_endpoint, json=registration_data)
        if response.status_code == 200:
            print("Registration successful!")
        else:
            print("Registration failed. Error:", response.text)

    def login(self, username, password):
        login_data = {"username": username, "password": password}
        response = requests.post(self.base_url + self.login_endpoint, json=login_data)
        if response.status_code == 200:
            print("Login successful!")
        else:
            print("Login failed. Error:", response.text)

    def delete_account(self, username, password):
        delete_account_data = {"username": username, "password": password}
        response = requests.delete(self.base_url + self.delete_account_endpoint, json=delete_account_data)
        if response.status_code == 200:
            print("Account deletion successful!")
        else:
            print("Account deletion failed. Error:", response.text)

    def run(self):
        try:
            with lock:
            # self.sock = socket.create_connection((self.hostname, self.port))
                with create_connection((HOST, PORT)) as s:
                    while args.threads > 0:
                        args.threads -= 1
                        # Generate random credentials
                        # username = self.fake.user_name()
                        username = self.fake.name()
                        # 'Lucy Cechtelar'
                        email = self.fake.email()
                        password = self.fake.password(length=10, special_chars=True, digits=True, upper_case=True, lower_case=True)                
                        # Send credentials
                        credentials = f'{email},{username},{password}\n'
                        s.sendall(credentials.encode())                      
                        # Receive authentication prompt
                        result = s.recv(1024).decode()
                        if 'login' in result:
                            self.users = {
                                'username': username,
                                'password': password,
                                'email': email
                            }                                          
                            credentials = f'{username},{password}\n'   
                            s.sendall(credentials.encode())
                        elif 'already' in result:
                            print(result, end='')
                        # Receive authentication result
                        # result = s.recv(1024).decode()
                        # print(result, end='')
                        if 'successful' in result:
                            print(f'Welcome {username}!')
                            while args.requests > 0:    
                                args.requests -= 1
                                try:
                                    # msg = input('> ')
                                    msg = self.fake.sentence()
                                    # 'Expedita at beatae voluptatibus nulla omnis.'
                                    if msg.strip().upper() == 'HELP':
                                        print_help()
                                        continue
                                    s.sendall((msg + '\n').encode())
                                    reply = s.recv(1024)
                                    if not reply:
                                        print('Server closed the connection.')
                                        break
                                    # print('Server:', reply.decode().strip())
                                    if msg.strip().upper() == 'QUIT':
                                        break
                                except (KeyboardInterrupt, EOFError):
                                    print('\nExiting.')
                                    break
                                except Exception as e:
                                    print(f'Error: {e}')
                                    break                                                    

        except error as e:
            print(f"Error during data exchange: {e}")   
            # raise e
            exit(1)                

def worker():
    message = "HELO"

    while True:
        # Get the task from teh work queue
        item = q.get()

        new_client = Client(item, args.ip, args.port, message)
        new_client.run()
        # Mark this task item done, thus removing it from the work queue
        q.task_done()

async def main():
    global args
    if args.ip:
        global HOST
        HOST = args.ip
    if args.port:
        global PORT
        PORT = args.port
    if args.size:
        global SIZE
        SIZE = args.size
    if args.threads:
        global THREADS
        THREADS = args.threads
    if args.requests:
        global REQUESTS
        REQUESTS = args.requests
    if args.requests < 1:
        print("Error: Number of requests must be at least 1.")
        return
    if args.size < 1:
        print("Error: Message size must be at least 1 KB.")
        return
    if args.threads < 1:
        print("Error: Number of threads must be at least 1.")
        return
    # if args.ip == "     

    if args.version:
        print("echo_client.py v1.0")
        return
    # Populate the work queue with a list of numbers as long as the total number of requests wished to be sent.
    # These queue items can be thought of as decrementing counters for the client thread workers.
    for item in range(args.requests):
        q.put(item)

    # Create a number of threads, given by the maxWorkerThread variable, to initiate clients and begin sending requests.
    # for i in range(args.threads):
    #     t = Thread(target=worker)
    #     t.daemon = True
    #     t.start()

    # Do not exit the main thread until the sub-threads complete their work queue
    # q.join()
 
    for i in range(args.threads):
        L = await asyncio.gather(
            # worker()
            asyncio.to_thread(worker)                
        )
 
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
                , default=50
                , help = "number of threads"
                )
        parser.add_argument('-r', '--requests', default=50, type=int, help='Total number of requests to send to server')                
        
        args = parser.parse_args () # parse the command line
        asyncio.run(main())
    except KeyboardInterrupt:
        print ('Script interrupted')
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0) 
