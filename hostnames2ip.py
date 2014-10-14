#!/usr/bin/env python

import getopt, sys, socket, os, json

names = ""
results = ""
verbose = False

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
    print "Usage: "+sys.argv[0]+" -i <liste> -o <fichier> [-v]"
    print "OR: "+sys.argv[0]+" -f <fichier> -o <fichier> [-v]"
    print "  -h, --help\t\taffiche ce message"
    print "  -i, --input=\t\tliste de hostnames"
    print "  -f, --input-file=\t\tfichier de hostnames"
    print "  -o, --output=\t\tfichier de sortie"
    print "  -v, --verbose=\t\taffiche la sortie"

# Verification des parametres
try:
    opts, args = getopt.getopt(sys.argv[1:], "hi:f:o:v", ["help", "input=", "input-file=", "output=", "verbose"])
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
    elif opt in ("-v", "--verbose"):
        verbose = True
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

if verbose:
    print json.dumps(values, indent=4, sort_keys=True)

with open(results, 'w') as out:
    json.dump(values, out)

sys.exit(0)
