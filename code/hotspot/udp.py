"""

 ~ ESP-32 // Micropython ~
 udp.py : Simple UDP clients and server (notably for OSC)

 Licence            : CC-NC-BY-SA 4.0
 Author             : Philippe Esling
                     <esling@ircam.fr>

"""
import socket
from osc.osc_message_builder import OscMessageBuilder
        
class OSCClient:
    """
    Generic class for defining a OSC client on ESP32.
    This class mostly relies on sockets to establish communication
    """
    
    def __init__(self,     
            host: str = '127.0.0.1',
            port: int = 2323):
        self.host = host
        self.port = port
        self.dest = (host, port)
        self.sock = None
        self.create_socket()
        
    def create_socket(self):
        """ Instantiate the client socket """
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send(self,
             msg):
        """ Send a message through the socket """
        print(msg)
        print(self.dest)
        self.sock.sendto(msg.encode(), self.dest)
        
    def send_osc(self, address: str, value: ArgValue) -> None:
        """ Send a message formatted for 

        Args:
            address: OSC address the message shall go to
            value: One or more arguments to be added to the message
        """
        builder = OscMessageBuilder(address=address)
        if value is None:
            values = []
        elif not isinstance(value, list) or isinstance(value, (str, bytes)):
            values = [value]
        else:
            values = value
        for val in values:
            builder.add_arg(val)
        msg = builder.build()
        self.sock.sendto(msg.dgram, self.dest)

    def close(self):
        if self.sock:
            self.sock.close()
            self.sock = None

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
            
class OSCServer:
    """
    Generic class for defining a UDP client on ESP32.
    This class mostly relies on sockets to establish communication
    """
    
    def __init__(self,     
            host: str = '127.0.0.1',
            port: int = 4242):
        self.host = host
        self.port = port

class UDPBrodcastClient:
    """
    Generic class for defining a UDP Broadcast client.
    This class is useful for implementing our own mini-discovery algorithm
    """
    
    def __init__(self,     
            host: str = '255.255.255.255',
            port: int = 7374):
        self.host = host
        self.port = port
        self.dest = (host, port)
        self.sock = None
        self.create_socket()
        
    def create_socket(self):
        print("Creating broadcast client socket")
        """ Instantiate the client socket """
        if not self.sock:
            # Create a UDP socket
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            # Enable port reusage (able to run multiple clients and servers on single (host, port)). 
            # self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
            # Enable broadcasting mode
            self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
            self.sock.bind(("", self.port))
            
    def receive(self):
        print("Waiting for inbound broadcast IP ...")
        # Receive message containing IP
        data, addr = self.sock.recvfrom(1024)
        data = str(data, 'utf-8')
        print("Received ~broadcasted~ message: %s"%data)
        return data
        
class OSCManager:
    """
    Key class for OSCServers linking Python and Max / MSP

    Example :
    >>> server = OSCServer(1234, 1235) # Creating server
    >>> server.run() # Running server

    NB ; HOW TO AUTOMATIC DISCOVERY OF HOST IP ?
    Broadcast channel + Metro 100 ms : send IP ^^

    """
    
    # attributes automatically bounded to OSC ports
    osc_attributes = []
    
    # Initialization method
    def __init__(self,
            out_port: int = 2323,
            in_port: int = 4242,
            bc_port: int = 7374,
            host = '127.0.0.1',
            discovery: int = 1):
        super(OSCServer, self).__init__()
        # Server properties
        self.debug = False
        self.in_port = in_port
        self.out_port = out_port
        self.host = host
        self.discovery = discovery
        # Initialize
        if (discovery):
            # Auto-discovery of server
            self.discover(bc_port)
        # Creation of client
        self.client = OSCClient(self.host, self.out_port)
        # Send an init message to the server
        self.client.send_osc("/welcome", [])
        # Bindings for server
        #self.init_bindings(self.osc_attributes)
        #self.server = osc_server.BlockingOSCUDPServer((ip, in_port), self.dispatcher)
            
    def discover(self, bc_port: int = 7374):
        """ Procedure for automatic device discovery """
        # 1. Connect to broadcast
        broad_cli = UDPBrodcastClient(port = bc_port)
        # 2. Receive IP from laptop
        self.host = broad_cli.receive()
        self.host = str(self.host, 'utf-8').split('\x00')[0]
        print("Found broadcast host " + self.host)
        
    def send_osc(self, address: str, value: ArgValue) -> None:
        self.client.send_osc(address, value)
        


# OSC decorator
def osc_parse(func):
    '''decorates a python function to automatically transform args and kwargs coming from Max'''
    def func_embedding(address, *args):
        t_args = tuple(); kwargs = {}
        for a in args:
            if issubclass(type(a), str):
                if "=" in a:
                    key, value = a.split("=")
                    kwargs[key] = value
                else:
                    t_args = t_args + (a,)
            else:
                t_args = t_args + (a,)
        return func(*t_args, **kwargs)
    return func_embedding

# Helper function to parse attribute
def osc_attr(obj, attribute):
    def closure(*args):
        args = args[1:]
        if len(args) == 0:
            return getattr(obj, attribute)
        else:
            return setattr(obj, attribute, *args)
    return closure

def max_format(v):
    '''Format some Python native types for Max'''
    if issubclass(type(v), (list, tuple)):
        if len(v) == 0:
            return ' "" '
        return ''.join(['%s '%(i) for i in v])
    else:
        return v

def dict2str(dic):
    '''Convert a python dict to a Max message filling a dict object'''
    str = ''
    for k, v in dic.items():
        str += ', set %s %s'%(k, max_format(v))
    return str[2:]
