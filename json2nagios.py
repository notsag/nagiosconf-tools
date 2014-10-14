#!/usr/bin/env python

import getopt, sys, urllib2, json

data = ""

def check_http(host, ssl=False):
    if ssl:
        url = 'https://' + host
    else: url = 'http://' + host
    try:
        connection = urllib2.urlopen(url)
        print url + " : " + str(connection.getcode())
        connection.close()
    except urllib2.HTTPError:
        return False
    except urllib2.URLError:
        return False
    return True

# Aide
def usage():
    print "Usage: "+sys.argv[0]+" -i <fichier>"
    print "  -h, --help\t\taffiche ce message"
    print "  -i, --input=\t\tfichier json genere par hostnames2ip.py"

# Verification des parametres
try:
    opts, args = getopt.getopt(sys.argv[1:], "hi:", ["help", "input=", "input-file="])
except getopt.GetoptError as err:
    print str(err)
    usage()
    sys.exit(2)

for opt,arg in opts:
    if opt in ("-h", "--help"):
        usage()
        sys.exit(0)
    elif opt in ("-i", "--input"):
        data = arg
    else:
        sys.exit(2)

if data == "":
    usage()
    sys.exit(2)

# On parse le fichier
json_data = open(data, 'r')
data = json.load(json_data)
json_data.close()

# Pour chaque IP on verifie les ports 80 et 443
for row in data['data']:
    print row[u'ip']
    for url in row[u'hosts']:
        check_http(url)
        check_http(url, ssl=True)


#TODO CREATE NAGIOS CONF

sys.exit(0)
