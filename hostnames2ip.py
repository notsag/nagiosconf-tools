#!/usr/bin/env python

import getopt, sys, socket

names = ""
results = ""

# Conversion d'un hostname en adresse IP
def host2ip(hostname):
    return socket.gethostbyname(hostname)

# Aide
def usage():
    print "Usage: "+sys.argv[0]+" -i <fichier> -o <fichier>"
    print "  -h, --help\taffiche ce message"
    print "  -i, --input=\tliste de hostnames"
    print "  -o, --output=\tfichier de sortie"

# Vérification des paramètres
try:
    opts, args = getopt.getopt(sys.argv[1:], "hi:o:", ["help", "input=", "output="])
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
    elif opt in ("-o", "--output"):
        results = arg
    else:
        sys.exit(2)

if (names == "" or results == ""):
    usage()
    sys.exit(2)

# Conversion
for host in names.split():
    print host + " : " + host2ip(host)

sys.exit(0)
