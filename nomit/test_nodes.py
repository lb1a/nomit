"""

"""

import xml.etree.ElementTree as et

from nose.tools import *

import nodes
import descriptors


element_string = et.fromstring("<node attr='astring'>string</node>")
element_int = et.fromstring("<node attr='2'>1</node>") 
element_float = et.fromstring("<node attr='2.2'>1.1</node>")
element_bool = et.fromstring("<node attr='2'>1</node>")

element_subnode_string = et.fromstring("<node><subnode attr='astring'>string</subnode></node>")
element_subnode_int = et.fromstring("<node><subnode attr='2'>1</subnode></node>") 
element_subnode_float = et.fromstring("<node><subnode attr='2.2'>1.1</subnode></node>")
element_subnode_bool = et.fromstring("<node><subnode attr='2'>1</subnode></node>")

element_subnodes_string = et.fromstring("<node><subnode attr='astring'>stringa</subnode><subnode attr='bstring'>stringb</subnode></node>")
element_subnodes_int = et.fromstring("<node><subnode attr='21'>22</subnode><subnode attr='31'>32</subnode></node>") 
element_subnodes_float = et.fromstring("<node><subnode attr='2.1'>2.2</subnode><subnode attr='3.1'>3.2</subnode></node>")
element_subnodes_bool = et.fromstring("<node><subnode attr='21'>22</subnode><subnode attr='31'>32</subnode></node>")

element_monit = et.fromstring(open("test_monit.xml").read())


class SubNode(nodes._Base):
    s = descriptors._TextDescriptor(str, xpath="subnode")
    i = descriptors._TextDescriptor(int, xpath="subnode")
    f = descriptors._TextDescriptor(float, xpath="subnode")
#    b = descriptors._TextDescriptor(bool, xpath="subnode")
    sa = descriptors._AttributeDescriptor("attr", str, xpath="subnode")
    ia = descriptors._AttributeDescriptor("attr", int, xpath="subnode")
    fa = descriptors._AttributeDescriptor("attr", float, xpath="subnode")
#    ba = descriptors._AttributeDescriptor("attr", bool, xpath="subnode")
    
class Node(nodes._Base):
    s = descriptors._TextDescriptor(str)
    i = descriptors._TextDescriptor(int)
    f = descriptors._TextDescriptor(float)
#    b = descriptors._TextDescriptor(bool)
    sa = descriptors._AttributeDescriptor("attr", str)
    ia = descriptors._AttributeDescriptor("attr", int)
    fa = descriptors._AttributeDescriptor("attr", float)
#    ba = descriptors._AttributeDescriptor("attr", bool)
    
class XNode(Node):
    sn = descriptors._NodeDescriptor(Node, "subnode")
    sl = descriptors._NodeListDescriptor(Node, "subnode")

# -------------------------------------------------------------------

class Test60Monit(object):
    monit = nodes.Monit(element_monit)
    
    def test10_monit_id(self):
        assert self.monit.id == "4e5402c4c2754f41485b929e27efbd5d"
        
    def test10_monit_incarnation(self):
        assert self.monit.incarnation == 1349390711
    
    def test10_monit_version(self):
        assert self.monit.version == "5.4"
        
    def test20_monit_server_instance(self):
        assert isinstance(self.monit.server, nodes.Server)
        
    def test20_monit_server_values(self):
        assert self.monit.server.uptime == 148
        assert self.monit.server.poll == 60
        assert self.monit.server.startdelay == 0
        assert self.monit.server.localhostname == "centos63a"
        assert self.monit.server.controlfile == "/etc/monit.conf"
        assert isinstance(self.monit.server.httpd, nodes.Httpd)

    def test20_monit_platform_instance(self):
        assert isinstance(self.monit.platform, nodes.Platform)
        
    def test20_monit_platform_values(self):
        assert self.monit.platform.name == "Linux"
        assert self.monit.platform.release == "2.6.32-279.el6.x86_64"
        assert self.monit.platform.version == "#1 SMP Fri Jun 22 12:19:21 UTC 2012"
        assert self.monit.platform.machine == "x86_64"
        assert self.monit.platform.cpu == 1
        assert self.monit.platform.memory == 1020696
        assert self.monit.platform.swap == 262136
    
    def test20_monit_httpd_instance(self):
        assert isinstance(self.monit.server.httpd, nodes.Httpd)
        
    def test20_monit_httpd_values(self):
        assert self.monit.server.httpd.address == "localhost"
        assert self.monit.server.httpd.port == 2812
        assert self.monit.server.httpd.ssl == False
    
    def test20_monit_services_count(self):
        assert len(self.monit.services) == 2
    
    def test20_monit_services_instances(self):
        for s in self.monit.services:
            assert isinstance(s, nodes.Service)
            
    def test20_monit_service1_value(self):
        assert self.monit.services[1].name == "bin"
        assert self.monit.services[1].type == 1 
        assert self.monit.services[1].collected_sec == 1349390831
        assert self.monit.services[1].collected_usec == 733654
        assert self.monit.services[1].status == 0
        assert self.monit.services[1].status_hint == 0
        assert self.monit.services[1].monitor == 1
        assert self.monit.services[1].monitormode == 0
        assert self.monit.services[1].pendingaction == 0
            
    def test20_monit_events_instances(self):
        for e in self.monit.events:
            assert isinstance(e, nodes.Event)
            
    def test20_monit_events_count(self):
        assert len(self.monit.events) == 1
        
    def test20_monit_event0_values(self):
        assert self.monit.events[0].collected_sec == 1349390859
        assert self.monit.events[0].collected_usec == 878383
        assert self.monit.events[0].service == "Monit"
        assert self.monit.events[0].type == 5
        assert self.monit.events[0].id == 65536
        assert self.monit.events[0].state == 2
        assert self.monit.events[0].action == 3
        assert self.monit.events[0].message == "Monit stopped"
            

# -------------------------------------------------------------------

class Test50NodeListDescriptor(object):
    def test_default_xpath(self):
        d = descriptors._NodeDescriptor(Node)
        assert d.class_ == Node
        assert d.xpath == "*"
        
    def test_xpath(self):
        d = descriptors._NodeDescriptor(Node, "subnode")
        assert d.class_ == Node
        assert d.xpath == "subnode"
        
    def test_nodes_class(self):
        assert isinstance(XNode(element_subnodes_string).sl[0], Node)
        assert isinstance(XNode(element_subnodes_string).sl[1], Node)
        
    def test_nodes_values(self):
        assert XNode(element_subnodes_string).sl[0].s == "stringa"
        assert XNode(element_subnodes_string).sl[0].sa == "astring"
        assert XNode(element_subnodes_string).sl[1].s == "stringb"
        assert XNode(element_subnodes_string).sl[1].sa == "bstring"
    
    @raises(IndexError)
    def test_nodes_index_error(self):
        XNode(element_subnodes_string).sl[2]
         

class Test40NodeDescriptor(object):
    def test_default_xpath(self):
        d = descriptors._NodeDescriptor(Node)
        assert d.class_ == Node
        assert d.xpath == "*"
        
    def test_xpath(self):
        d = descriptors._NodeDescriptor(Node, "subnode")
        assert d.class_ == Node
        assert d.xpath == "subnode"
        
    def test_node_class(self):
        assert isinstance(XNode(element_subnode_string).sn, Node)
        
    def test_node_values(self):
        assert XNode(element_subnode_string).sn.s == "string"
        assert XNode(element_subnode_string).sn.sa == "astring"  

# -------------------------------------------------------------------

class Test10TextDescriptor(object):
        
    def test_default_conv(self):
        d = descriptors._TextDescriptor()
        assert d.conv == str
        assert d.xpath == "."
        
    def test_int_conv(self):
        d = descriptors._TextDescriptor(int)
        assert d.conv == int
        assert d.xpath == "."
        
    def test_float_conv(self):
        d = descriptors._TextDescriptor(float)
        assert d.conv == float
        assert d.xpath == "."
        
    def test_string_conv(self):
        d = descriptors._TextDescriptor(str)
        assert d.conv == str
        assert d.xpath == "."
        
#     def test_bool_conv(self):
#         d = descriptors._TextDescriptor(bool)
#         assert d.conv == bool
#         assert d.xpath == "."
        
    def test_default_conv_xpath(self):
        d = descriptors._TextDescriptor(xpath="//subnode")
        assert d.conv == str
        assert d.xpath == "//subnode"
        
        
    def test_int_conv_xpath(self):
        d = descriptors._TextDescriptor(int, xpath="//subnode")
        assert d.conv == int
        assert d.xpath == "//subnode"
        
    def test_float_conv_xpath(self):
        d = descriptors._TextDescriptor(float, xpath="//subnode")
        assert d.conv == float
        assert d.xpath == "//subnode"
        
    def test_string_conv_xpath(self):
        d = descriptors._TextDescriptor(str, xpath="//subnode")
        assert d.conv == str
        assert d.xpath == "//subnode"
        
#     def test_bool_conv_xpatht(self):
#         d = descriptors._TextDescriptor(bool, xpath="//subnode")
#         assert d.conv == bool 
#         assert d.xpath == "//subnode"    
        
        
    def test_descriptor_int(self):
        assert Node(element_int).i == 1
        
    def test_descriptor_string(self):
        assert Node(element_string).s == "string"
        assert Node(element_int).s == "1"
        assert Node(element_bool).s == "1"
        assert Node(element_float).s == "1.1"
        
    def test_descriptor_float(self):
        assert Node(element_float).f == 1.1
        
#     def test_descriptor_bool(self):
#         assert Node(element_bool).b == True
        
    
    def test_descriptor_subnode_int(self):
        assert SubNode(element_subnode_int).i == 1
        
    def test_descriptor_subnode_string(self):
        assert SubNode(element_subnode_string).s == "string"
        assert SubNode(element_subnode_int).s == "1"
        assert SubNode(element_subnode_bool).s == "1"
        assert SubNode(element_subnode_float).s == "1.1"
        
    def test_descriptor_subnode_float(self):
        assert SubNode(element_subnode_float).f == 1.1
        
#     def test_descriptor_subnode_bool(self):
#         assert SubNode(element_subnode_bool).b == True

# -------------------------------------------------------------------   
    
class Test20AttributeDescriptor(object):
        
    def test_default_conv(self):
        d = descriptors._AttributeDescriptor("attr")
        assert d.conv == str
        assert d.xpath == "."
        
    def test_int_conv(self):
        d = descriptors._AttributeDescriptor("attr", int)
        assert d.conv == int
        assert d.xpath == "."
        
    def test_float_conv(self):
        d = descriptors._AttributeDescriptor("attr", float)
        assert d.conv == float
        assert d.xpath == "."
        
    def test_string_conv(self):
        d = descriptors._AttributeDescriptor("attr", str)
        assert d.conv == str
        assert d.xpath == "."
        
#     def test_bool_conv(self):
#         d = descriptors._AttributeDescriptor("attr", bool)
#         assert d.conv == bool
#         assert d.xpath == "."
        
    def test_default_conv_xpath(self):
        d = descriptors._AttributeDescriptor("attr", xpath="//subnode")
        assert d.conv == str
        assert d.xpath == "//subnode"
        
        
    def test_int_conv_xpath(self):
        d = descriptors._AttributeDescriptor("attr", int, xpath="//subnode")
        assert d.conv == int
        assert d.xpath == "//subnode"
        
    def test_float_conv_xpath(self):
        d = descriptors._AttributeDescriptor("attr", float, xpath="//subnode")
        assert d.conv == float
        assert d.xpath == "//subnode"
        
    def test_string_conv_xpath(self):
        d = descriptors._AttributeDescriptor("attr", str, xpath="//subnode")
        assert d.conv == str
        assert d.xpath == "//subnode"
        
#     def test_bool_conv_xpatht(self):
#         d = descriptors._AttributeDescriptor("attr", bool, xpath="//subnode")
#         assert d.conv == bool 
#         assert d.xpath == "//subnode"    
        
        
    def test_descriptor_int(self):
        assert Node(element_int).ia == 2
         
    def test_descriptor_string(self):
        assert Node(element_string).sa == "astring"
        assert Node(element_int).sa == "2"
        assert Node(element_bool).sa == "2"
        assert Node(element_float).sa == "2.2"
         
    def test_descriptor_float(self):
        assert Node(element_float).fa == 2.2
         
#     def test_descriptor_bool(self):
#         assert Node(element_bool).ba == True
         
     
    def test_descriptor_subnode_int(self):
        assert SubNode(element_subnode_int).ia == 2
         
    def test_descriptor_subnode_string(self):
        assert SubNode(element_subnode_string).sa == "astring"
        assert SubNode(element_subnode_int).sa == "2"
        assert SubNode(element_subnode_bool).sa == "2"
        assert SubNode(element_subnode_float).sa == "2.2"
         
    def test_descriptor_subnode_float(self):
        assert SubNode(element_subnode_float).fa == 2.2
         
#     def test_descriptor_subnode_bool(self):
#         assert SubNode(element_subnode_bool).ba == True