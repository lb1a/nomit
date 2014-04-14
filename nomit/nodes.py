"""
nomit.nodes.py

Classes representing the different XML nodes.

"""

try:
    import xml.etree.cElementTree as et
except ImportError:
    import xml.etree.ElementTree as et

import descriptors
import constants

class _Base(object):
    """
    Base class for all other node classes.
    
    """
    
    element = None
    
    def __init__(self, element):
        self.element = element


class Httpd(_Base):
    """
    Represent <httpd> node, and children.
    
    <httpd>
      <address>localhost</address>
      <port>2812</port>
      <ssl>0</ssl>
    </httpd>

    """
    
    address = descriptors._TextDescriptor(conv=str, xpath="address")
    port = descriptors._TextDescriptor(conv=int, xpath="port")
    ssl = descriptors._TextDescriptor(conv=int, xpath="ssl")
    
    def __repr__(self):
        return "[httpd address=%s, port=%s, ssl=%s]" % (self.address, self.port, self.ssl)
    

class Server(_Base):
    """
    Represent <server> node, attributes and children.
    
    <server>
        <uptime>148</uptime>
        <poll>60</poll>
        <startdelay>0</startdelay>
        <localhostname>centos63a</localhostname>
        <controlfile>/etc/monit.conf</controlfile>
        <httpd>
          ...
        </httpd>
    </server>

    """
    
    uptime = descriptors._TextDescriptor(conv=int, xpath="uptime")
    poll = descriptors._TextDescriptor(conv=int, xpath="poll")
    startdelay = descriptors._TextDescriptor(conv=int, xpath="startdelay")
    localhostname = descriptors._TextDescriptor(conv=str, xpath="localhostname")
    controlfile = descriptors._TextDescriptor(conv=str, xpath="controlfile")
    httpd = descriptors._NodeDescriptor(Httpd, "httpd", default=None)
    
    def __repr__(self):
        return "[server uptime=%s, poll=%s, startdelay=%s, localhostname=%s, controlfile=%s, httpd=%s]" % (
            self.uptime, self.poll, self.startdelay, self.localhostname, self.controlfile, self.httpd)


class Platform(_Base):
    """
    Represent <platform> node and children.
    
    <platform>
        <name>Linux</name>
        <release>2.6.32-279.el6.x86_64</release>
        <version>#1 SMP Fri Jun 22 12:19:21 UTC 2012</version>
        <machine>x86_64</machine>
        <cpu>1</cpu>
        <memory>1020696</memory>
        <swap>262136</swap>
    </platform>

    """
    
    name = descriptors._TextDescriptor(conv=str, xpath="name")
    release = descriptors._TextDescriptor(conv=str, xpath="release")
    version = descriptors._TextDescriptor(conv=str, xpath="version")
    machine = descriptors._TextDescriptor(conv=str, xpath="machine")
    cpu = descriptors._TextDescriptor(conv=int, xpath="cpu")
    memory = descriptors._TextDescriptor(conv=int, xpath="memory")
    swap = descriptors._TextDescriptor(conv=int, xpath="swap")
    
    def __repr__(self):
        return "[platform name=%s, release=%s, version=%s, machine=%s, cpu=%s, memory=%s, swap=%s]" % (
                self.name, self.release, self.version, self.machine,self.cpu, self.memory, self.swap)


class Every(_Base):
    # TODO: implement Every class
    pass

class HostIcmp(_Base):
    """
    Represent an <icmp> node of a host <service>.
    
    <icmp>
        <type>Echo Request</type>
        <responsetime>0.000</responsetime>
    </icmp>
    
    """
    
    type = descriptors._TextDescriptor(conv=str, xpath="type")
    responsetime = descriptors._TextDescriptor(conv=float, xpath="responsetime")
    
    def __repr__(self):
        return "{icmp type=%s, responsetime=%s}" % (self.type, self.responsetime)
    
        
class ProcessMemory(_Base):
    """
    Represent a <memory> node of a process <service>.
    
    <memory>
        <percent>0.1</percent>
        <percenttotal>33.2</percenttotal>
        <kilobyte>1220</kilobyte>
        <kilobytetotal>339184</kilobytetotal>
    </memory>
    
    """
    
    percent = descriptors._TextDescriptor(conv=float, xpath="percent")
    percenttotal = descriptors._TextDescriptor(conv=float, xpath="percenttotal")
    kilobyte = descriptors._TextDescriptor(conv=int, xpath="kilobyte")
    kilobytetotal = descriptors._TextDescriptor(conv=int, xpath="kilobytetotal")
    
    
    def __repr__(self):
        return "[memory percent=%s, percenttotal=%s, kilobyte=%s, kilobytetotal=%s]" % (
                   self.percent, self.percenttotal, self.kilobyte, self.kilobytetotal)


class ProcessCpu(_Base):
    """
    Represent a <cpu> node of a process <service>.
     
    <cpu>
        <percent>0.0</percent>
        <percenttotal>15.8</percenttotal>
    </cpu>
     
    """
     
    percent = descriptors._TextDescriptor(conv=float, xpath="percent")
    percenttotal = descriptors._TextDescriptor(conv=float, xpath="percenttotal")
     
     
    def __repr__(self):
        return "[cpu percent=%s, percenttotal=%s]" % (self.percent, self.percenttotal)


class ProcessPort(_Base):
    """
    Represent a <port> node of a process <service>.
    
    <service name="NAME">
        <type>5</type>
        ...
        <port>
            <hostname>127.0.0.1</hostname>
            <portnumber>123</portnumber>
            <request/>
            <protocol>DEFAULT</protocol>
            <type>UDP</type>
            <responsetime>1.234</responsetime>
        </port>
    </service>
    
    """
    
    hostname = descriptors._TextDescriptor(conv=str, xpath="hostname")
    portnumber = descriptors._TextDescriptor(conv=int, xpath="portnumber")
    request = descriptors._TextDescriptor(conv=str, xpath="request")
    protocol = descriptors._TextDescriptor(conv=str, xpath="protocol")
    type = descriptors._TextDescriptor(conv=str, xpath="type")
    responsetime = descriptors._TextDescriptor(conv=float, xpath="responsetime")
    
    def __repr__(self):
        return "[port hostname=%s, portnumber=%s, request=%s, protocol=%s, type=%s, responsetime=%s" % (
                   self.hostname, self.portnumber, self.request, self.protocol, self.type, self.responsetime)
    
    
class ProcessUnix(_Base):
    """
    <unix>
        <path>%s</path>
        <protocol>%s</protocol>
        <responsetime>%.3f</responsetime>
    </unix>
    
    """
    
    # TODO: implement UnixPort class 


HostPort = ProcessPort
HostUnix = ProcessUnix


class SystemLoad(_Base):
    """
    Represent a <load> node of a system <service>.
    
    <service name="NAME">
        <type>5</type>
        ...
        <system>
            <load>
                <avg01>0.07</avg01>
                <avg05>0.02</avg05>
                <avg15>0.00</avg15>
            </load>
        </system>
    </service>
     
    """
     
    avg01 = descriptors._TextDescriptor(conv=float, xpath="avg01")
    avg05 = descriptors._TextDescriptor(conv=float, xpath="avg05")
    avg15 = descriptors._TextDescriptor(conv=float, xpath="avg15")
     
     
    def __repr__(self):
        return "[load avg01=%s, avg05=%s, avg15=%s]" % (self.avg01, self.avg05, self.avg15)
    

class SystemCpu(_Base):
    """
    Represent a <cpu> node of a system <service>.
    
    <service name="SYSTEM">
        <type>5</type>
        ...
        <system>
            <cpu>
                <user>13.7</user>
                <system>1.5</system>
                <wait>0.6</wait>
            </cpu>
        </system>
    </service>
    
    """
    
    user = descriptors._TextDescriptor(conv=float, xpath="user")
    system = descriptors._TextDescriptor(conv=float, xpath="system")
    wait = descriptors._TextDescriptor(conv=float, xpath="wait")
     
     
    def __repr__(self):
        return "[cpu user=%s, system=%s, wait=%s]" % (self.user, self.system, self.wait)
    
    
class SystemMemory(_Base):
    """
    Represent a <memory> node of a system <service>.
    
    <service name="SYSTEM">
        <type>5</type>
        ...
        <system>
            <memory>
                <percent>35.3</percent>
                <kilobyte>360668</kilobyte>
            </memory>
        </system>
    </service>
    
    """
    
    percent = descriptors._TextDescriptor(conv=float, xpath="percent")
    kilobyte = descriptors._TextDescriptor(conv=int, xpath="kilobyte")
     
     
    def __repr__(self):
        return "[memory percent=%s, kilobyte=%s]" % (self.percent, self.kilobyte)
    

class SystemSwap(SystemMemory):
    """
    Represent a <swap> node of a system <service>.
    
    <service name="SYSTEM">
        <type>5</type>
        ...
        <system>
            <swap>
                <percent>0.0</percent>
                <kilobyte>0</kilobyte>
            </swap>
        </system>
    </service>
    
    """
    
    percent = descriptors._TextDescriptor(conv=float, xpath="percent")
    kilobyte = descriptors._TextDescriptor(conv=int, xpath="kilobyte")
      
    def __repr__(self):
        return "{swap percent=%s, kilobyte=%s}" % (self.percent, self.kilobyte)


class ProgramProgram(_Base):
    """
    Represent a <program> node of a program <service>
    
    <program>
        <started>1396173854</started>
        <status>0</status>
    </program>
    
    """
    
    started = descriptors._TextDescriptor(conv=int, xpath="started")
    status = descriptors._TextDescriptor(conv=int, xpath="status")
    
    def __repr__(self):
        return "{program started=%s, status=%s}" % (self.started, self.status)
    
    
class FilesystemBlock(_Base):
    """
    <block> node inside a filesystem <service>.
    
    <block>
        <percent>43.3</percent>
        <usage>2802.2</usage>
        <total>7315.3</total>
    </block>
        
    """
    
    percent = descriptors._TextDescriptor(conv=float, xpath="percent")
    usage = descriptors._TextDescriptor(conv=float, xpath="usage")
    total = descriptors._TextDescriptor(conv=float, xpath="total")
    
    def __repr__(self):
        return "{block percent=%s, usage=%s, total=%s}" % (self.percent, self.usage, self.total)
    
    
class FilesystemInode(_Base):
    """
    <inode> node inside a filesystem <service>.
    
    <inode>
        <percent>16.5</percent>
        <usage>78608</usage>
        <total>475776</total>
    </inode>
    
    """
    
    percent = descriptors._TextDescriptor(conv=float, xpath="percent")
    usage = descriptors._TextDescriptor(conv=int, xpath="usage")
    total = descriptors._TextDescriptor(conv=int, xpath="total")
    
    def __repr__(self):
        return "{inode percent=%s, usage=%s, total=%s}" % (self.percent, self.usage, self.total)
    
    
class Service(_Base):
    """
    Represent <service> node, attributes and children.
    
    <service name="ALL SERVICES">
        ...
        <collected_sec>1349390831</collected_sec>
        <collected_usec>733654</collected_usec>
        <status>0</status>
        <status_hint>0</status_hint>
        <monitor>1</monitor>
        <monitormode>0</monitormode>
        <pendingaction>0</pendingaction>
        ...
        <every>
            <type>3</type>
            <cron>* 0-3 * * 0</cron>
            </every>
    </service>
    
    
    <service name="FILESYSTEM">
        <type>0</type>
        ...
        <mode>555</mode>
        <uid>0</uid>
        <gid>0</gid>
        <flags>4096</flags>
        <block>
            <percent>43.3</percent>
            <usage>2802.2</usage>
            <total>7315.3</total>
        </block>
        <inode>
            <percent>16.5</percent>
            <usage>78608</usage>
            <total>475776</total>
        </inode>
    </service>
    
    
    <service name="DIRECTORY">
        <type>1</type>
        ...
        <mode>755</mode>
        <uid>0</uid>
        <gid>0</gid>
        <timestamp>1396074312</timestamp>
    </service>
    
    
    <service name="FILE">
        <type>2</type>
        ...
        <mode>755</mode>
        <uid>0</uid>
        <gid>0</gid>
        <timestamp>1394689057</timestamp>
        <size>2826</size>
        <checksum type="MD5">026d168a317c6177a8998215f4541b8c</checksum>
    </service>
    
    <service name="PROCESS">
        <type>3</type>
        ...
        <pid>966</pid>
        <ppid>1</ppid>
        <uptime>173305</uptime>
        <children>13</children>
        <memory>
            <percent>0.1</percent>
            <percenttotal>33.2</percenttotal>
            <kilobyte>1220</kilobyte>
            <kilobytetotal>339184</kilobytetotal>
        </memory>
        <cpu>
            <percent>0.0</percent>
            <percenttotal>15.8</percenttotal>
        </cpu>
        <port>
            <hostname>127.0.0.1</hostname>
            <portnumber>123</portnumber>
            <request/>
            <protocol>DEFAULT</protocol>
            <type>TCP</type>
            <responsetime>-1.000</responsetime>
        </port>
        <port>
            ...
        </port>
    </service>
        
    
    <service name="host.localhost">
        <type>4</type>
        ...
        <icmp>
            <type>Echo Request</type>
            <responsetime>0.000</responsetime>
        </icmp>
        <icmp>
            ...
        </icmp>
        <port>
            <hostname>127.0.0.1</hostname>
            <portnumber>80</portnumber>
            <request>/data/show</request>
            <protocol>HTTP</protocol>
            <type>TCP</type>
            <responsetime>-1.000</responsetime>
        </port>
        <port>
            ...
        </port>
    </service>
    
    
    <service name="SYSTEM">
        <type>5</type>
        ...
        <system>
            <load>
                <avg01>0.07</avg01>
                <avg05>0.02</avg05>
                <avg15>0.00</avg15>
            </load>
            <cpu>
                <user>13.7</user>
                <system>1.5</system>
                <wait>0.6</wait>
            </cpu>
            <memory>
                <percent>35.3</percent>
                <kilobyte>360668</kilobyte>
            </memory>
            <swap>
                <percent>0.0</percent>
                <kilobyte>0</kilobyte>
            </swap>
        </system>
    </service>
    
    
    <service name="FIFO">
        <type>6</type>
        ...
        <mode>644</mode>
        <uid>0</uid>
        <gid>0</gid>
        <timestamp>1396172864</timestamp>
    </service>
        
        
    <service name="PROGRAM">
        <type>7</type>
        <program>
            <started>1396173854</started>
            <status>0</status>
        </program>
    </service>
    
    """
    
    # All services
    #
    name = descriptors._AttributeDescriptor("name")
    type = descriptors._TextDescriptor(conv=int, xpath="type")
    collected_sec = descriptors._TextDescriptor(conv=int, xpath="collected_sec")
    collected_usec = descriptors._TextDescriptor(conv=int, xpath="collected_usec")
    status = descriptors._TextDescriptor(conv=int, xpath="status")
    status_hint = descriptors._TextDescriptor(conv=int, xpath="status_hint")
    monitor = descriptors._TextDescriptor(conv=int, xpath="monitor")
    monitormode = descriptors._TextDescriptor(conv=int, xpath="monitormode")
    pendingaction = descriptors._TextDescriptor(conv=int, xpath="pendingaction")
    # Provide collected_sec.collected_usec as a float for convenience
    collected = property(lambda self: float("%d.%d" % (self.collected_sec, self.collected_usec)))
    
    
    # Type 0 - Filesystem
    #
    _filesystem_mode = descriptors._TextDescriptor(conv=str, xpath="mode")
    _filesystem_uid = descriptors._TextDescriptor(conv=int, xpath="uid")
    _filesystem_gid = descriptors._TextDescriptor(conv=int, xpath="gid")
    _filesystem_flags = descriptors._TextDescriptor(conv=int, xpath="flags")
    _filesystem_block = descriptors._NodeDescriptor(FilesystemBlock, "block")
    _filesystem_inode = descriptors._NodeDescriptor(FilesystemInode, "inode")
    
    
    # Type 1 - Directory
    #
    _dir_mode = descriptors._TextDescriptor(conv=str, xpath="mode")
    _dir_uid = descriptors._TextDescriptor(conv=int, xpath="uid")
    _dir_gid = descriptors._TextDescriptor(conv=int, xpath="gid")
    _dir_timestamp = descriptors._TextDescriptor(conv=int, xpath="timestamp")
    
    
    # Type 2  - File
    #
    _file_mode = descriptors._TextDescriptor(conv=str, xpath="mode")
    _file_uid = descriptors._TextDescriptor(conv=int, xpath="uid")
    _file_gid = descriptors._TextDescriptor(conv=int, xpath="gid")
    _file_size = descriptors._TextDescriptor(conv=int, xpath="size")
    _file_timestamp = descriptors._TextDescriptor(conv=int, xpath="timestamp")
    _file_checksum =  descriptors._TextDescriptor(conv=str, xpath="checksum")
    _file_checksum_type = descriptors._AttributeDescriptor("type", xpath="checksum")
    
    
    # Type 3 - Process
    #
    _process_pid = descriptors._TextDescriptor(conv=int, xpath="pid")
    _process_ppid = descriptors._TextDescriptor(conv=int, xpath="ppid")
    _process_uptime = descriptors._TextDescriptor(conv=int, xpath="uptime")
    _process_children = descriptors._TextDescriptor(conv=int, xpath="children")
    _process_memory = descriptors._NodeDescriptor(ProcessMemory, "memory", default=None)
    _process_cpu = descriptors._NodeDescriptor(ProcessCpu, "cpu", default=None)
    _process_ports = descriptors._NodeListDescriptor(ProcessPort, "port")
    
    
    # Type 4 - Host
    #
    _host_ports = descriptors._NodeListDescriptor(HostPort, "port")
    _host_icmp = descriptors._NodeListDescriptor(HostIcmp, "icmp")
    
    
    # Type 5 - System
    #
    _system_load = descriptors._NodeDescriptor(SystemLoad, "system/load", default=None)
    _system_cpu  = descriptors._NodeDescriptor(SystemCpu, "system/cpu", default=None)
    _system_memory  = descriptors._NodeDescriptor(SystemMemory, "system/memory", default=None)
    _system_swap  = descriptors._NodeDescriptor(SystemSwap, "system/swap", default=None)
    
    
    # Type 6 - FIFO 
    #
    _fifo_mode = _dir_mode
    _fifo_uid = _dir_uid
    _fifo_gid = _dir_gid
    _fifo_timestamp = _dir_timestamp
    
    
    # Type 7 - Program
    #
    _program_program = descriptors._NodeDescriptor(ProgramProgram, "program")
    
    
    @property
    def pid(self):
        if self.type == constants.TYPE_PROCESS:
            return self._process_pid
        else:
            raise AttributeError
        
    @property
    def ppid(self):
        if self.type == constants.TYPE_PROCESS:
            return self._process_ppid
        else:
            raise AttributeError
        
    @property
    def uptime(self):
        if self.type == constants.TYPE_PROCESS:
            return self._process_uptime
        else:
            raise AttributeError
        
    @property
    def children(self):
        if self.type == constants.TYPE_PROCESS:
            return self._process_children
        else:
            raise AttributeError
        
    @property
    def ports(self):
        if self.type == constants.TYPE_PROCESS:
            return self._process_ports
        elif self.type == constants.TYPE_HOST:
            return self._host_ports
        else:
            raise AttributeError
        
    @property
    def memory(self):
        if self.type == constants.TYPE_PROCESS:
            return self._process_memory
        elif self.type == constants.TYPE_SYSTEM:
            return self._system_memory
        else:
            raise AttributeError
        
    @property
    def cpu(self):
        if self.type == constants.TYPE_PROCESS:
            return self._process_cpu
        elif self.type == constants.TYPE_SYSTEM:
            return self._system_cpu
        else:
            raise AttributeError
        
    @property
    def load(self):
        if self.type == constants.TYPE_SYSTEM:
            return self._system_load
        else:
            raise AttributeError
        
    @property
    def swap(self):
        if self.type == constants.TYPE_SYSTEM:
            return self._system_swap
        else:
            raise AttributeError
        
    @property
    def mode(self):
        if self.type == constants.TYPE_FILE:
            return self._file_mode
        elif self.type == constants.TYPE_DIRECTORY:
            return self._dir_mode
        elif self.type == constants.TYPE_FIFO:
            return self._fifo_mode
        elif self.type == constants.TYPE_FILESYSTEM:
            return self._filesystem_mode
        else:
            raise AttributeError
        
    @property
    def uid(self):
        if self.type == constants.TYPE_FILE:
            return self._file_uid
        elif self.type == constants.TYPE_DIRECTORY:
            return self._dir_uid
        elif self.type == constants.TYPE_FIFO:
            return self._fifo_uid
        elif self.type == constants.TYPE_FILESYSTEM:
            return self._filesystem_uid
        else:
            raise AttributeError
        
    @property
    def gid(self):
        if self.type == constants.TYPE_FILE:
            return self._file_gid
        elif self.type == constants.TYPE_DIRECTORY:
            return self._dir_gid
        elif self.type == constants.TYPE_FIFO:
            return self._fifo_gid
        elif self.type == constants.TYPE_FILESYSTEM:
            return self._filesystem_gid
        else:
            raise AttributeError
        
    @property
    def timestamp(self):
        if self.type == constants.TYPE_FILE:
            return self._file_timestamp
        elif self.type == constants.TYPE_DIRECTORY:
            return self._dir_timestamp
        elif self.type == constants.TYPE_FIFO:
            return self._fifo_timestamp
        else:
            raise AttributeError
        
    @property
    def size(self):
        if self.type == constants.TYPE_FILE:
            return self._file_size
        else:
            raise AttributeError
        
    @property
    def checksum(self):
        if self.type == constants.TYPE_FILE:
            return self._file_checksum
        else:
            raise AttributeError
        
    @property
    def checksum_type(self):
        if self.type == constants.TYPE_FILE:
            return self._file_checksum_type
        else:
            raise AttributeError
        
    @property
    def icmp(self):
        if self.type == constants.TYPE_HOST:
            return self._host_icmp
        else:
            raise AttributeError
    icmps = icmp
    
    @property
    def program(self):
        if self.type == constants.TYPE_PROGRAM:
            return self._program_program
        else:
            raise AttributeError
        
    @property
    def flags(self):
        if self.type == constants.TYPE_FILESYSTEM:
            return self._filesystem_flags
        
    @property
    def block(self):
        if self.type == constants.TYPE_FILESYSTEM:
            return self._filesystem_block
        
    @property
    def inode(self):
        if self.type == constants.TYPE_FILESYSTEM:
            return self._filesystem_inode
    
    
    def __repr__(self):
        
        s = "{service name=%s, type=%s, collected=%s, status=%s, status_hint=%s, monitor=%s, monitormode=%s, pendingaction=%s" % (
                       self.name, self.type, self.collected, self.status, 
                       self.status_hint, self.monitor, self.monitormode, self.pendingaction)
        
        if self.type == constants.TYPE_FILESYSTEM:
            s += " mode=%s, uid=%s, gid=%s, flags=%s, block=%s, inode=%s}" % (
                    self.mode, self.uid, self.gid, self.flags, self.block, self.inode)
        elif self.type == constants.TYPE_DIRECTORY:
            s +=  " mode=%s, uid=%s, gid=%s, timestamp=%s}" % (
                    self.mode, self.uid, self.gid, self.timestamp)
        elif self.type == constants.TYPE_FILE:
            s += " mode=%s, uid=%s, gid=%s, timestamp=%s, size=%s, checksum=(%s)%s}" % (
                    self.mode, self.uid, self.gid, self.timestamp, self.size, self.checksum_type, self.checksum)
        elif self.type == constants.TYPE_PROCESS:
            s += " pid=%s, ppid=%s, uptime=%s, children=%s, memory=%s, cpu=%s, ports=%s}" % (
                    self.pid, self.ppid, self.uptime, self.children, self.memory, self.cpu, self.ports)
        elif self.type == constants.TYPE_HOST:
            s += " ports=%s, icmps=%s}" % (self.ports, self.icmps)
        elif  self.type == constants.TYPE_SYSTEM:
            s += " load=%s, cpu=%s, memory=%s, swap=%s}" % (
                    self.load, self.cpu, self.memory, self.swap)
        elif self.type == constants.TYPE_FIFO:
            s += " mode=%s, uid=%s, gid=%s, timestamp=%s}" % (
                    self.mode, self.uid, self.gid, self.timestamp)
        elif self.type == constants.TYPE_PROGRAM:
            s += " program=%s}" % (self.program)
        else:
            raise ValueError("%s not a known service type" % (self.type))
            
        return s
    

class Event(_Base):
    """
    Represent <event> node and children.
    
    <event>
        <collected_sec>1349390859</collected_sec>
        <collected_usec>878383</collected_usec>
        <service>Monit</service>
        <type>5</type>
        <id>65536</id>
        <state>2</state>
        <action>3</action>
        <message>Monit stopped</message>
    </event>
    
    """
    
    collected_sec = descriptors._TextDescriptor(conv=int, xpath="collected_sec")
    collected_usec = descriptors._TextDescriptor(conv=int, xpath="collected_usec")
    service = descriptors._TextDescriptor(conv=str, xpath="service")
    type = descriptors._TextDescriptor(conv=int, xpath="type")
    id = descriptors._TextDescriptor(conv=int, xpath="id")
    state = descriptors._TextDescriptor(conv=int, xpath="state")
    action = descriptors._TextDescriptor(conv=int, xpath="action")
    message = descriptors._TextDescriptor(conv=str, xpath="message")
    
    def __repr__(self):
        return "[event collected=%s.%s, service=%s, type=%s, id=%s, state=%s, action=%s, message=%s]" % (
                    self.collected_sec, self.collected_usec, self.service, self.type, self.id, self.state, self.action, self.message)


class Servicegroup(_Base):
    """
    Represent a <servicegroup> node and children.
    
    <servicegroup name="group.system">
        <service>ntpd</service>
        <service>cron_rc</service>
        <service>cron</service>
    </servicegroup>
        
    """
    
    name = descriptors._AttributeDescriptor("name")
    services = property(lambda self: [e.text for e in self.element.findall("service")])
    
    def __repr__(self):
        return "[servicegroup name=%s services=%s" % (self.name, self.services)
    
    
class Monit(_Base):
    """
    Represent <monit> node, attributes and children.
    
    """
    
    id = descriptors._AttributeDescriptor("id")
    """<monit id="4e5402c4c2754f41485b929e27efbd5d" ...>"""
    incarnation = descriptors._AttributeDescriptor("incarnation", int)
    """<monit ... incarnation="1349390711" ...>"""
    version = descriptors._AttributeDescriptor("version")
    """<monit ... version="5.4">"""
    server = descriptors._NodeDescriptor(Server, "server")
    """<monit><server>...</server></monit>"""
    platform = descriptors._NodeDescriptor(Platform, "platform")
    """<monit><server>...</server></monit>"""
    services = descriptors._NodeListDescriptor(Service, "services/service")
    """<monit>...<services><service></service>...</services></monit>"""
    servicegroups = descriptors._NodeListDescriptor(Servicegroup, "servicegroups/servicegroup")
    """<monit>...<servicegroup><servicegroup></servicegroup>...</servicegroup></monit>"""
    events = descriptors._NodeListDescriptor(Event, "event")
    """<monit>...<event></event>...</monit>"""
    
    def __repr__(self):
        return "[monit id=%s, incarnation=%s, version=%s, server=%s, platform=%s, services=%s, servicegroups=%s, events=%s" % (
                   self.id, self.incarnation, self.version, self.server, self.platform, self.services, self.servicegroups, self.events)

