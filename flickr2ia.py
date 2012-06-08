#!/home/jake/.virtualenvs/default/bin/python
import urllib2
import os
import yaml
import simplejson as json
import datetime
from collections import defaultdict

ROOT_DIR = os.getcwd()
PHOTO_DIR = os.path.join(ROOT_DIR, 'nasahqphoto')


#______________________________________________________________________________
def get_coverage(location_dict):
    location = {k: v for (k,v) in location_dict.iteritems() if v}
    if location.get('latitude'):
        coverage = "%s %s" % (location['latitude'], location['longitude'])
    if location.get('neighbourhood'):
        if coverage: coverage = coverage + '; ' + location['neighbourhood']['_content']
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
    print coverage

#______________________________________________________________________________
def exists_on_ia(flickr_ids):
    oldid = "%s_%s" % flickr_ids
    possible_ids = ([oldid + "_o", oldid + "_b", oldid + "_z",
                     "nasahqphoto-flickr-%s" % flickr_ids[0]])
    for id in possible_ids:
        meta_url = 'http://archive.org/metadata/%s' % id
        j = json.loads(urllib2.urlopen(meta_url).read())
        if j:
            return True
    return False

#______________________________________________________________________________
items = [x for x in os.listdir('nasahqphoto') if x.endswith('info.yaml')]
for item in items:
    info_file = os.path.join(PHOTO_DIR, item)
    meta_dict = yaml.load(open(info_file).read())['photo']
    flickr_ids = (meta_dict['id'], meta_dict['originalsecret'])
    if exists_on_ia(flickr_ids):
        continue
    identifier = "nasa-flickr-%s" % meta_dict['id']
    description = meta_dict['description']['_content']
    date = meta_dict['dates']['taken'].strftime('%Y-%m-%d')
    subject = '; '.join([x['raw'] for x in meta_dict['tags']['tag']])
    source = meta_dict['urls']['url'][0]['_content']
    title = meta_dict['title']
    coverage = get_coverage(meta_dict['location'])

    license_map = {"1": "http://creativecommons.org/licenses/by-nc-sa/2.0/",
                   "2": "http://creativecommons.org/licenses/by-nc/2.0/",
                   "3": "http://creativecommons.org/licenses/by-nc-nd/2.0/",
                   "4": "http://creativecommons.org/licenses/by/2.0/",
                   "5": "http://creativecommons.org/licenses/by-sa/2.0/",
                   "6": "http://creativecommons.org/licenses/by-nd/2.0/",
                   "7": "http://flickr.com/commons/usage/"}
    licenseurl = license_map[meta_dict['license']]
    print licenseurl


    #print "\n\n----\n\n"
    #for k,v in meta_dict.iteritems():
    #    print "%s\t=>\t%s" % (k,v)
