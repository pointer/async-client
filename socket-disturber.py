__version__ = "1.0.0"
__doc__     = """High traffic generator to load switch for the switch demonstration"""

import threading
from ctypes import *
import socket
import argparse
import textwrap
import sys
import os
from signal import signal, SIGPIPE, SIG_DFL
signal(SIGPIPE,SIG_DFL)
#// ln -s /...libboostSourceFiles.../libboost_thread.so /..RequestTOmtFiles.../libboost_thread-mt.so
args = None

class disturb_class(threading.Thread):
    def __init__ (self, sock):
        threading.Thread.__init__(self)
        self.sock = sock
        
    def run(self):
        disturb(self.sock)
        

def disturb(sock):
    try:
        ip = args.IP
        port = args.port
        # sock.connect((ip, port))
        buf = bytes()
        for i in range(args.size): # args.size cycles of 1024 bytes messages
            v = (c_byte * (1024))(1 % 0x111111111) #1024 bytes
            buf += bytearray(v) 
        # try:
        #     sock.connect((ip, port))
        #     sock.send(buf)
            
        # except socket.error:
        #     print(f"socket setup error: {socket.error}")
        try:
            ## Send data to the server  
            sock.sendto(buf, (ip, port))
            # print(f"Sent: {message}")

            ## Receive data from the server
            data = sock.recv(1024)
            print(f"Received: {data.decode('utf-8')}")
        except socket.error as e:
            print(f"Error during data exchange: {e}")            
        finally:
            pass
            ## Clean up the connection
            # sock.close()
            # print(f"Socket closed")    
    except socket.timeout:
        print(f"Connection attempt timed out")
    except ConnectionRefusedError:
        print(f"Connection refused. Make sure the server is running.")
    except socket.error as e:
        print(f"Connection error: {e}")            

def main():
    
    if args.version :
        print( "switch_disturber.py v%s" % (__version__, ) )
        sys.exit(0)

    try: 
        print ("Socket created. Start sending messages")
        # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print (f'Destination: {args.IP}:{args.port}')
        print (f'Message size: {args.size} kb. Number of threads: {args.threads}')
        print("\nCtrl+C to break")
        
        while(1):
            threads = []
            for num in range(0, args.threads): # num of threads
                thread = disturb_class(sock)
                thread.start()
                threads.append(thread)
            for thread in threads:
                thread.join()
    except socket.error:
        print("socket setup error")

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
        parser = argparse.ArgumentParser \
            ( formatter_class=argparse.ArgumentDefaultsHelpFormatter
            , description = textwrap.dedent (description)
            , epilog = textwrap.dedent (example_of_use)
            )

        parser.add_argument \
                ( "-v", "--version"
                , action = "store_true"
                , help = "show program's version number and exit"
                )

        parser.add_argument \
                ( "-i", "--IP"
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
        
        args = parser.parse_args () # parse the command line
        main()
    except KeyboardInterrupt:
        print ('Script interrupted')
    try:
        sys.exit(0)
    except SystemExit:
        os._exit(0) 