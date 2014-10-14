#!/usr/bin/env python

import getopt, sys, urllib2, json

data = ""
BASECONF_HOST="define host {\nuse\tgeneric-host,ssh\ncontact_groups\tadmins\nhost_name\tHOSTNAME\naddress\tIPADDRESS\n}\n"
BASECONF_SERVICE="define service {\nuse\tgeneric-service\nhost_name\tHOSTNAME\nservice_description\tURL\ncheck_command\tCOMMAND\n}\n"

# Verification de la reponse HTTP/HTTPs
def check_http(host, ssl=False):
    if ssl:
        url = 'https://' + host
    else: url = 'http://' + host
    try:
        connection = urllib2.urlopen(url)
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

# Pour chaque IP
for row in data['data']:
    # Le hostname dans nagios correspond au premier nom
    hn = row[u'hosts'][0]
    config_f = open(hn+'.cfg', 'w')
    config_host = BASECONF_HOST.replace('IPADDRESS', row[u'ip']).replace('HOSTNAME', hn)
    # On verifie que le nom repond en http et https
    for url in row[u'hosts']:
        config_services = ""
        # Si reponse HTTP on cree le service http
        if check_http(url):
            config_services = config_services + BASECONF_SERVICE.replace('HOSTNAME', hn).replace('URL', url).replace('COMMAND', 'check_myhttp!'+url)
        # Si reponse HTTPs on cree les services https et https_certificate
        if check_http(url, ssl=True):
            config_services = config_services + BASECONF_SERVICE.replace('HOSTNAME', hn).replace('URL', url).replace('COMMAND', 'check_myhttps!'+url)
            config_services = config_services + BASECONF_SERVICE.replace('HOSTNAME', hn).replace('URL', url).replace('COMMAND', 'check_myhttps_certificate!'+url)
    # On concatene conf host et services puis on ecrit le fichier
    conf = config_host + config_services
    config_f.write(conf)
    config_f.close()

sys.exit(0)
