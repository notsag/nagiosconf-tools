#!/usr/bin/env python

import getopt, sys, socket, os

names = ""
results = ""

# Conversion d'un hostname en adresse IP
def host2ip(hostname):
    return socket.gethostbyname(hostname)

def groupbyip(host):
    ip = host2ip(host)
    if ip in values.keys():
        values[ip].append(host)
    else:
        values[ip] = [host]

# Aide
def usage():
    print "Usage: "+sys.argv[0]+" -i <liste> -o <fichier>"
    print "OR: "+sys.argv[0]+" -f <fichier> -o <fichier>"
    print "  -h, --help\t\taffiche ce message"
    print "  -i, --input=\t\tliste de hostnames"
    print "  -f, --input-file=\t\tfichier de hostnames"
    print "  -o, --output=\t\tfichier de sortie"

# Verification des parametres
try:
    opts, args = getopt.getopt(sys.argv[1:], "hi:f:o:", ["help", "input=", "input-file=", "output="])
except getopt.GetoptError as err:
    print str(err)
    usage()
    sys.exit(2)

for opt,arg in opts:
    if opt in ("-h", "--help"):
        usage()
        sys.exit(0)
    elif opt in ("-i", "--input"):
        names = arg
    elif opt in ("-f", "--input-file"):
        names = arg
    elif opt in ("-o", "--output"):
        results = arg
    else:
        sys.exit(2)

if (names == "" or results == ""):
    usage()
    sys.exit(2)

values = dict()

# Conversion
if not os.path.isfile(names):
    # Cas d'une liste de hosts
    for host in names.split():
        groupbyip(host)
else:
    # Cas d'un fichier
    f = open(names, 'r')
    for host in f:
        host = host.rstrip()
        groupbyip(host)
    f.close()

print values

sys.exit(0)
