#Name: io_handlers.py
#Author: Will Barnes
#Purpose: Handle XML input and output

#Import needed modules
import logging
import numpy as np
import xml.etree.ElementTree as ET
import xml.dom.minidom as xdm

class InputHandler(object):
    """General classs for handling XML input files.
    
    Attributes:
        root -- root element for tree of input file
        var_list -- list of strings of variables to be read
        input_dict -- dictionary of input values as read from XML file
        
    """
    
    def __init__(self,input_filename,input_vars,**kwargs):
        """Initialize InputHandler class."""
        
        #Create XML tree and root node
        tree = ET.parse(input_filename)
        self.root = tree.getroot()
        #Set variable list as attribute
        self.var_list = input_vars
        #Initialize dictionary to hold results of input parameters
        self.input_dict = {}
        #Start logging
        logger = logging.getLogger(type(self).__name__)
        
        
    def lookup_vars(self,**kwargs):
        """Loop over var_list and find XML node value."""
        
        for var in self.var_list:
            #Find node
            node = self.root.find(var)
            #Check if found
            if node is None:
                logger.warning("No value found for input %s"%var)
                logger.warning("Check for consistency between XML node and variable list.")
                continue
            
            #check node type
            node_type = node.get('type')
            #loop over children if node is a parent
            if node_type == type(np.array([])).__name__ or node_type == type([]).__name__:
                temp =[]
                for child in node:
                    temp.append(self.set_type(child))
                    
                #set dictionary field
                self.input_dict[node.tag] = np.array(temp)
            #otherwise just get the value
            else:
                self.input_dict[node.tag] = self.set_type(node)
                
            
    def set_type(self,node,**kwargs):
        """Set node value depending on type"""
        
        node_type = node.get('type')
        if node_type == type(str()).__name__:
            val = node.text
        elif node_type == type(float()).__name__ or node_type == type(np.float64()).__name__:
            val = float(node.text)
        elif node_type == type(int()).__name__ or node_type == type(np.int64()).__name__:
            val = int(note.text)
        else:
            logger.warning("Missing or unknown type for node %s"%node.tag)
            logger.warning("Reading in as string.")
            val = node.text
            
        return val
        
        
        
class OutputHandler(object):
    """General class for handling printing of output files from Python dictionaries.
    Can be used to print both configuration files as well as results files. Print to 
    either plain text or structured XML files.
    
    Attributes:
        output_filename -- string containing filename to print to
        output_dict -- dictionary to print to file
        
    """
    
    def __init__(self,output_filename,output_dict,**kwargs):
        """Initialize OutputHandler class"""
        
        self.output_filename = output_filename
        self.output_dict = output_dict
        
        
    def print_to_xml(self):
        """Print dictionary to XML file"""
        
        root = ET.Element('root')
        for key in self.output_dict:
            if (type(self.output_dict[key]) is not np.ndarray) and (type(self.output_dict[key]) is not list):
                self.set_element(root,key,self.output_dict[key])
            else:
                element = ET.SubElement(root,key)
                for i in range(len(self.output_dict[key])):
                    self.set_element(element,key+str(i),self.output_dict[key][i])
                    
        with open(self.output_filename,'w') as f: 
            f.write(self.pretty_print_xml(root))
            
        f.close()
            
            
    def set_element(self,root,name,val):
        """Create element, set tag, set value."""
        
        element = ET.SubElement(root,name)
        element.text = str(val)
        element.set('type',type(val).__name__)
        
        
    def pretty_print_xml(self,element):
        """Formatted XML output for writing to file."""
        
        unformatted = ET.tostring(element)
        xdmparse = xdm.parseString(unformatted)
        return xdmparse.toprettyxml(indent="    ")
        
        
        
        
        
        
        
        
        
        
        
        
        
            