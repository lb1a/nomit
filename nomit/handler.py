"""


"""

# TODO: M/Monit: error receiving data from http://localhost:2811/ -- Resource temporarily unavailable
# TODO: Create Server class that the user is meant to derive from

import socket
import sys
import BaseHTTPServer
import SocketServer
try:
    import xml.etree.cElementTree as et
except ImportError:
    import xml.etree.ElementTree as et

import nodes
import handlers


# The different modes the server can operate in. By default the
# server will handle POST requests sequentially.
#
THREADING = 1
FORKING = 2


# Node handlers are available as global variables so that 
# `HttpPostHandler.do_POST` has access to them.
#
_RAW_HANDLER = None
_MONIT_HANDLER = None
_HTTPD_HANDLER = None
_SERVER_HANDLER = None
_PLATFORM_HANDLER = None
_SERVICE_HANDLER = None
_SERVICEGROUP_HANDLER = None
_EVENT_HANDLER = None


class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

class ForkingTCPServer(SocketServer.ForkingMixIn, SocketServer.TCPServer):
    pass




class HttpPostHandler(BaseHTTPServer.BaseHTTPRequestHandler):
    
    def finish(self,*args,**kw):
        """
        Re-write finish() to catch Broken Pipe errrors.
        http://stackoverflow.com/questions/6063416/python-basehttpserver-how-do-i-catch-trap-broken-pipe-errors
        
        """
        
        try:
            if not self.wfile.closed:
                self.wfile.flush()
                self.wfile.close()
          
        except socket.error:
            pass
          
        self.rfile.close()
        
        
    def log_message(self, fmt, *args):
        """
        Suppress logging of requests.
        
        """
        
        return

    
    def do_POST(self):
        """
        
        """
        
        # Read all request data from client
        #
        data = self.rfile.read() 

        # Send 200 OK and headers. This is fine with the client (Monit)
        # but crashes here. We simply ignore that. TODO: does sending 200 still crash?
        #
        try:
            self.send_response(200) 
        except:
            pass


        # Find the <monit>...</monit> section in the POST
        #
        try: 
            start_pos = data.find("<monit")
            end_pos = data.find("</monit>")
            xml = data[start_pos:end_pos+8]
        except IndexError:
            return
        
        print data
        
    
        # Convert the XML into an Element
        #
        element = et.fromstring(xml)
        monit = nodes.Monit(element)
        
        
        # Iterate through the nodes and call the handlers.
        #
        _RAW_HANDLER(data)
        _MONIT_HANDLER(monit)
        _SERVER_HANDLER(monit.server)
        _HTTPD_HANDLER(monit.server.httpd)
        _PLATFORM_HANDLER(monit.platform)

        for servicegroup in monit.servicegroups:
            _SERVICEGROUP_HANDLER(servicegroup)

        for service in monit.services:
            _SERVICE_HANDLER(service)
            
        for event in monit.events:
            _EVENT_HANDLER(event)


def run(address=("127.0.0.1", 2811), raw_handler=handlers._null_handler,
        monit_handler=handlers._null_handler, httpd_handler=handlers._null_handler,
        server_handler=handlers._null_handler, platform_handler=handlers._null_handler,
        service_handler=handlers._null_handler, servicegroup_handler=handlers._null_handler,
        event_handler=handlers._null_handler, mode=None):
    """
    Listen on `address` for HTTP-POST from 'Monit' instances.
    
    """
    
    # Register the event handlers for the nodes as global variables 
    # so that `HttpPostHandler.do_POST` has access to them.
    #
    global _RAW_HANDLER
    global _MONIT_HANDLER
    global _HTTPD_HANDLER
    global _SERVER_HANDLER
    global _PLATFORM_HANDLER
    global _SERVICE_HANDLER
    global _SERVICEGROUP_HANDLER
    global _EVENT_HANDLER
    
    _RAW_HANDLER = raw_handler
    _MONIT_HANDLER = monit_handler
    _HTTPD_HANDLER = httpd_handler
    _SERVER_HANDLER = server_handler
    _PLATFORM_HANDLER = platform_handler
    _SERVICE_HANDLER = service_handler
    _SERVICEGROUP_HANDLER = servicegroup_handler
    _EVENT_HANDLER = event_handler
    
    
    # Determine server mode
    #
    if mode == THREADING:
        server = ThreadedTCPServer(address, HttpPostHandler)
    elif mode == FORKING:
        server = ForkingTCPServer(address, HttpPostHandler)
    else:
        server = SocketServer.TCPServer(address, HttpPostHandler)
    
    
    # Run forevere
    #
    server.serve_forever()
    

if __name__ == "__main__":
        
    import handlers
    
    run(raw_handler=handlers._debug_handler,
        monit_handler=handlers._debug_handler,
        server_handler=handlers._debug_handler,
        platform_handler=handlers._debug_handler,
        httpd_handler=handlers._debug_handler,
        service_handler=handlers._debug_handler,
        event_handler=handlers._debug_handler)
