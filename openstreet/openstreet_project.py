
# coding: utf-8

# In[1]:

import os
import xml.etree.cElementTree as ET
from collections import defaultdict
import pprint
import re
import codecs
import json
import string
from pymongo import MongoClient


# In[2]:

'''
import xml.etree.ElementTree as ET  # Use cElementTree or lxml if too slow

OSM_FILE = "pittsburgh_pennsylvania.osm"  # Replace this with your osm file
SAMPLE_FILE = "sample.osm"

ks = 60 # Parameter: take every k-th top level element

def get_element(osm_file, tags=('node', 'way', 'relation')):
    """Yield element if it is the right type of tag

    Reference:
    http://stackoverflow.com/questions/3095434/inserting-newlines-in-xml-file-generated-via-xml-etree-elementtree-in-python
    """
    context = iter(ET.iterparse(osm_file, events=('start', 'end')))
    _, root = next(context)
    for event, elem in context:
        if event == 'end' and elem.tag in tags:
            yield elem
            root.clear()


with open(SAMPLE_FILE, 'wb') as output:
    output.write('<?xml version="1.0" encoding="UTF-8"?>\n')
    output.write('<osm>\n  ')

    # Write every kth top level element
    for i, element in enumerate(get_element(OSM_FILE)):
        if i % ks == 0:
            output.write(ET.tostring(element, encoding='utf-8'))

    output.write('</osm>')

'''


# In[3]:

filename = "pittsburgh_data.osm" # osm filename
path = "/home/sumit/Desktop/data_analyst_nanodegree/investigate/doubt" # directory contain the osm file
final_data = os.path.join(path, filename)

# some regular expression 
lower = re.compile(r'^([a-z]|_)*$') 
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


# In[4]:

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", "Trail", "Parkway", "Commons"]


# In[5]:

def tagscount(filename):
        tags = {}
        for _, elem in ET.iterparse(filename):
            if elem.tag in tags: 
                tags[elem.tag] += 1
            else:
                tags[elem.tag] = 1
        return tags
final_data_tags = tagscount(final_data)
pprint.pprint(final_data_tags)


# In[6]:


 #Categories distrubution and finding tag count
def process_map(filename):                     
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}  
    for _, element in ET.iterparse(filename):
        if element.tag == "tag":
             for tag in element.iter('tag'):
                    k = tag.get('k')
                    if lower.search(k) :
                        keys['lower'] += 1 
                    elif lower_colon.search(k):
                        keys['lower_colon'] += 1
                    elif problemchars.search(k):
                        keys['problemchars'] += 1
                    else :
                        keys['other'] += 1
    return keys

final_data_keys = process_map(final_data)
pprint.pprint(final_data_keys)


# # Auditing the street names

# In[7]:

def audit_street_type(street_types, street_name):
    # add unexpected street name to a list
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)
            
def is_street_name(elem):
    # determine whether a element is a street name
    return (elem.attrib['k'] == "addr:street")

def audit_street(osmfile):
    # iter through all street name tag under node or way and audit the street name value
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    #audit_street_type(street_types, tag.attrib['v'])
                    m = street_type_re.search(tag.attrib['v'])
                    if m:
                        street_type = m.group()
                        if street_type not in expected:
                            street_types[street_type].add(tag.attrib['v'])
    return street_types


# In[8]:

street_types = audit_street(final_data)


# In[9]:

pprint.pprint(dict(street_types))


# In[10]:

mapping = { "Dr":"Drive",
            "Ct": "Court",
            "Way":"Way",
            "Plz":"Plaza",
            "Ln":"Lane",
            "Cres":"Crescent",
            "Ter":"Terrace",
            "Blvd":"Boulevard",
            "St": "Street",
            "st": "Street",
            "St.": "Street",
            "St,": "Street",
            "ST": "Street",
            "street": "Street",
            "Street.": "Street",
            "Ave": "Avenue",
            "Ave.": "Avenue",
            "ave": "Avenue",
            "Rd.": "Road",   
            "rd.": "Road",
            "Rd": "Road",    
            "Hwy": "Highway",
            "HIghway": "Highway",
            "Pkwy": "Parkway",
            "Pl": "Place",      
            "place": "Place",
            "Sq.": "Square",
            
            }




# In[11]:


def namechange(old_name, mapping, regex):                         
    m = regex.search(old_name)
    if m:
        street_type = m.group()
        if street_type in mapping:
            old_name = re.sub(regex, mapping[street_type], old_name)     

    return old_name
 #iteratiion through the street names and fixing them
for _, ways in street_types.iteritems():      
    for temp in ways:
        newname = namechange(temp, mapping, street_type_re)
        
        print temp,"becomes", newname


# # Audit the Zip Codes

# In[12]:

'''
def is_zipcode(elem):
    return (elem.attrib['k'] == "addr:postcode")

def zips_audit(mapfile):
    # iter through all zip codes, collect all the zip codes that does not start with 02
    map_file = open(mapfile, "r")
    invalid_zips = defaultdict(set)
    for event, elem in ET.iterparse(map_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_zipcode(tag):
                    temp = tag.attrib['v']
                    twoDigits = temp[0:2]

                    if not re.match(r'^15{3}$', temp) : # match five digit strings that start with '96'
                        invalid_zips[twoDigits].add(temp)
    return invalid_zips          

   if  not tag.attrib['v'].startswith('94') and tag.attrib['k'] == "addr:postcode":
                    if tag.attrib['v'] not in zips:
                        zips[tag.attrib['v']] = 1
                    else:
                        zips[tag.attrib['v']] += 1 
                        #from collections import defaultdict    
'''
def zip_data_audit(invalid_zipcodes, zipcode):
    twoDigits = zipcode[0:2]        #validating zip code and adding it to invalid if not satisfying the conditions
    
    if not re.match(r'^15\d{3}$', zipcode): #match five digit strings that start with '96'
        invalid_zipcodes[twoDigits].add(zipcode)
        
def is_zipcode(elem):
    return (elem.attrib['k'] == "addr:postcode")  

def zipdata_audit(file_osm):
    osmdata = open(file_osm, "r")
    invalid_zipcodes = defaultdict(set)
    for _, elem in ET.iterparse(osmdata, events=("start",)): #calling audit_zipcode iterating on all the zipcodes

        if elem.tag == "way" or elem.tag == "node" :
            for tag in elem.iter("tag"):
                temp = tag.attrib['v']
                if tag.attrib['k'] == "addr:postcode":
                    zip_data_audit(invalid_zipcodes,temp)

    return invalid_zipcodes
                        
cd = zipdata_audit(final_data)    




# In[13]:

print cd


# In[14]:

def update_zip(zipcode):                          # Fixing zip codes in case it don't match the desired pattern.
    return (re.findall(r'\d{5}', zipcode))[0]
for street_type, ways in cd.iteritems():
    for name in ways:
        better_name = update_zip(name)
        print name, "=>", better_name


# # Process the openstreet XML

# In[15]:

CREATED = [ "version", "changeset", "timestamp", "user", "uid"]

def update_name(name, mapping):
    updated = []
    
    for portion in name.split(" "):
        
        portion = portion.strip(",\.").lower()
                
        if portion in mapping.keys():
        
            portion = mapping[portion]
        
        updated.append(portion.capitalize())
    
    return " ".join(updated)

def shape_element(element):
    node = {}
    node["created"]={}
    node["address"]={}
    node["pos"]=[]
    refs=[]
    
    # we only process the node and way tags
    if element.tag == "node" or element.tag == "way" :
        if "id" in element.attrib:
            node["id"]=element.attrib["id"]
        node["type"]=element.tag

        if "visible" in element.attrib.keys():
            node["visible"]=element.attrib["visible"]
      
        # the key-value pairs with attributes in the CREATED list are added under key "created"
        for elem in CREATED:
            if elem in element.attrib:
                node["created"][elem]=element.attrib[elem]
                
        # attributes for latitude and longitude are added to a "pos" array
        # include latitude value        
        if "lat" in element.attrib:
            node["pos"].append(float(element.attrib["lat"]))
        # include longitude value    
        if "lon" in element.attrib:
            node["pos"].append(float(element.attrib["lon"]))

        
        for tag in element.iter("tag"):
            if not(problemchars.search(tag.attrib['k'])):
                if tag.attrib['k'] == "addr:housenumber":
                    node["address"]["housenumber"]=tag.attrib['v']
                    
                if tag.attrib['k'] == "addr:postcode":
                    node["address"]["postcode"]=tag.attrib['v']
                
                # handling the street attribute, update incorrect names using the strategy developed before   
                if tag.attrib['k'] == "addr:street":
                    node["address"]["street"]=tag.attrib['v']
                    node["address"]["street"] = update_name(node["address"]["street"], mapping)

                if tag.attrib['k'].find("addr")==-1:
                    node[tag.attrib['k']]=tag.attrib['v']
                    
        for nd in element.iter("nd"):
             refs.append(nd.attrib["ref"])
                
        if node["address"] =={}:
            node.pop("address", None)

        if refs != []:
           node["node_refs"]=refs
            
        return node
    else:
        return None

# process the xml openstreetmap file, write a json out file and return a list of dictionaries
def process_map(file_in, pretty = False):
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2)+"\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data


# In[ ]:

data = process_map(final_data, True)


# In[76]:

#pprint.pprint(dict(data))
data[352]


# # Insert the data into local MongoDB Database

# In[77]:

client = MongoClient()
db = client.openstreetdata
collection = db.openstreetMAP
collection.insert(data)


# In[78]:

collection


# In[79]:

#size of xml
os.path.getsize(final_data)


# In[80]:

#count of number of documents in Mongo DB
collection.find().count()     


# In[81]:

#Size Of json file
os.path.getsize("sample.osm.json")/1024/1024      


# In[82]:

#count of number of nodes
collection.find({"type":"node"}).count()


# In[83]:

#number of unique users
collection.find({"type":"way"}).count()


# In[84]:

#Top five users with most contributions
pipeline = [{"$group":{"_id": "$created.user",     
                       "count": {"$sum": 1}}},
            {"$sort": {"count": -1}},
            {"$limit": 5}]
result = collection.aggregate(pipeline)
x=list(result)
x


# GeoKitten is the most active user

# In[85]:

#Proportion of the top user contributions
top_user_prop = [{"$group":{"_id": "$created.user",
                       "count": {"$sum": 1}}},
            {"$project": {"proportion": {"$divide" :["$count",collection.find().count()]}}},
            {"$sort": {"proportion": -1}},
            {"$limit": 5}]
result = list(collection.aggregate(top_user_prop))
result


# 16% contribution was alone by GeoKitten.

# # Further exploration

# In[87]:

#Different schools situated in the city
pipeline = [{"$match":{"amenity":{"$exists":1}, "amenity": "school", "name":{"$exists":1}}},
            {"$group":{"_id":"$name", "count":{"$sum":1}}},
            {"$sort":{"count":-1}},{"$limit":10}]
result = list(collection.aggregate(pipeline))
result


# In[89]:

# mostly religion followed
pipeline = [{"$match":{"religion":{"$exists":1}}},
                      {"$group":{"_id":"$religion", "count":{"$sum":1}}},
                      {"$sort":{"count":-1}}]
result=list(collection.aggregate(pipeline)) 
result


# # Additional Information for data

# As most of the people enters information into the data there is a chance of human errors while typing. So proper validations must be used while entering the data. 
# Also user should be incentivized for the greater number of contributions. There should be ranking of users on the basis of contributions.
# The benefit of this is that the user will do more and more contribution for getting incentives.
