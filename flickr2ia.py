#!/home/jake/.virtualenvs/default/bin/python
import os
import datetime
import urllib2

import yaml
from lxml import etree


#______________________________________________________________________________
def get_coverage(location_dict):
    location = {k: v for (k,v) in location_dict.iteritems() if v}
    if location.get('latitude'):
        coverage = "%s %s" % (location['latitude'], location['longitude'])
    if location.get('neighbourhood'):
        if coverage: coverage = coverage + ', ' + location['neighbourhood']['_content']
        else: coverage = location['neighbourhood']['_content']
    if location.get('county'):
        if coverage: coverage = coverage + ', ' + location['county']['_content']
        else: coverage = location['county']['_content']
    if location.get('locality'):
        if coverage: coverage = coverage + ', ' + location['locality']['_content']
        else: coverage = location['locality']['_content']
    if location.get('country'):
        if coverage: coverage = coverage + ', ' + location['country']['_content']
        else: coverage = location['country']['_content']
    return coverage

#______________________________________________________________________________
def get_license(license_dict):
    license_map = {"0": None,
                   "1": "http://creativecommons.org/licenses/by-nc-sa/2.0/",
                   "2": "http://creativecommons.org/licenses/by-nc/2.0/",
                   "3": "http://creativecommons.org/licenses/by-nc-nd/2.0/",
                   "4": "http://creativecommons.org/licenses/by/2.0/",
                   "5": "http://creativecommons.org/licenses/by-sa/2.0/",
                   "6": "http://creativecommons.org/licenses/by-nd/2.0/",
                   "7": "http://flickr.com/commons/usage/"}
    return license_map[license_dict]

#______________________________________________________________________________
def mk_metadata(meta_dict, ITEM_DIR):
    fxml = os.path.join(ITEM_DIR, "%s_files.xml" % meta_dict['identifier'])
    f = open(fxml, "wb")
    f.write("<files />")
    f.close()
    root = etree.Element("metadata")
    for k,v in meta_dict.iteritems():
        subElement = etree.SubElement(root,k)
        subElement.text = v
    meta_xml = etree.tostring(root, pretty_print=True,
                              xml_declaration=True, encoding="utf-8")
    mxml = os.path.join(ITEM_DIR, "%s_meta.xml" % meta_dict['identifier'])
    ff = open(mxml, "wb")
    ff.write(meta_xml)
    ff.close()

#______________________________________________________________________________
ROOT_DIR = os.getcwd()
items = [x[0] for x in os.walk('nasahqphoto') if x[0] != 'nasahqphoto']
for item in items:
    try:
        identifier = item.split('/')[-1]
        print "CREATING::\t%s" % identifier
        ITEM_DIR = os.path.join(ROOT_DIR, 'nasahqphoto', identifier)
        info_file = os.path.join(ITEM_DIR, '%s_info.yaml' % identifier)
        comments_file = info_file.replace('_info.yaml', '_comments.yaml')
        exif_file = info_file.replace('_info.yaml', '_exif.yaml')
        people_file = info_file.replace('_info.yaml', '_people.yaml')
        tags_file = info_file.replace('_info.yaml', '_tags.yaml')
        og_photo = info_file.replace('_info.yaml', '.jpg')
        meta_dict = yaml.load(open(info_file).read())['photo']
        ia_meta = dict(identifier = "nasahqphoto-%s" % meta_dict['id'],
                       description = meta_dict['description']['_content'],
                       date = meta_dict['dates']['taken'].strftime('%Y-%m-%d'),
                       subject = '; '.join([x['raw'] for x in meta_dict['tags']['tag']]),
                       source = meta_dict['urls']['url'][0]['_content'],
                       title = meta_dict['title']['_content'],
                       coverage = get_coverage(meta_dict['location']),
                       license = get_license(meta_dict['license']),
                       mediatype = 'image',
                       collection = 'nasaheadquartersflickrstream',
                       creator = 'NASA')
        ia_meta = dict((k,v) for (k,v) in ia_meta.iteritems() if v)
        mk_metadata(ia_meta, ITEM_DIR)
    except:
        print "ERROR\t%s" % item
