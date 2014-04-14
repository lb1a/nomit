"""

"""

class _TextDescriptor(object):
    """
    Descriptor to extract the text of an XML node.
    
    This descriptor expects that the class using it has an attribute `element`
    which is an instance of `xml.etree.ElementTree.Element`. All classes
    in this module that represent nodes of a 'Monit' XML message do 
    have such an `element` attribute.
    
    """
    
    def __init__(self, conv=str, xpath=".", default=None):
        """
        :param conv: Conversion function.
        :param xpath: XPath to node.
         
        """
        
        self.conv = conv
        self.xpath = xpath
        self.default = default
    
        
    def __get__(self, instance, owner):
        """
        :return: The value of the text of the node found at `self.xpath` 
            converted by `self.conv`.
        
        """

        text = instance.element.findtext(self.xpath)
        
        if text:
            return self.conv(text.strip())
        else:
            if isinstance(self.default, Exception):
                raise self.default
            else:
                return self.default


class _AttributeDescriptor(object):
    """
    Descriptor to extract the value of an attribute of an XML node.
    
    This descriptor expects that the class using it has an attribute `element`
    which is an instance of `xml.etree.ElementTree.Element`. All classes
    in this module that represent nodes of a 'Monit' XML message do 
    have such an `element` attribute.
    
    """
    
    def __init__(self, attr, conv=str, xpath=".", default=None):
        """

        :param attr: Name of the node's attribute.
        :param conv: Conversion function.
        :param xpath: XPath to node.
        
        """
        
        self.attr = attr
        self.conv = conv        
        self.xpath = xpath
        self.default = default
        
    
    def __get__(self, instance, owner):
        """
        :return: The value of the attribute named `self.attr` of the 
            node found at `self.xpath` converted by `self.conv`.
        """
    
        attr = instance.element.attrib.get(self.attr)
        
        if attr:
            return self.conv(attr.strip())
        else:
            if isinstance(self.default, Exception):
                raise self.default
            else:
                return self.default


class _NodeDescriptor(object):
    """
    Descriptor to return a single XML node.
    
    This descriptor expects that the class using it has an attribute `element`
    which is an instance of `xml.etree.ElementTree.Element`. All classes
    in this module that represent nodes of a 'Monit' XML message do 
    have such an `element` attribute.
    
    """
    
    def __init__(self, class_, xpath="*", default=None):
        """
        
        :param class_: Class whose instance shall be returned.
        :param xpath: XPath to child node. 
         
        """
        
        self.class_ = class_
        self.xpath = xpath
        self.default = default
    
        
    def __get__(self, instance, owner):
        """
        :return: Instance of `self.class` of the  node found at `self.xpath`.
        
        """
        
        node = instance.element.find(self.xpath)
        
        if node:
            return self.class_(node)
        else:
            if isinstance(self.default, Exception):
                raise self.default
            else:
                return self.default



class _NodeListDescriptor(_NodeDescriptor):
    
    def __get__(self, instance, owner):
        """
        :return: List of instance of `self.class` of the  nodes found at `self.xpath`.
        
        """
        
        return [self.class_(n) for n in instance.element.findall(self.xpath)]
