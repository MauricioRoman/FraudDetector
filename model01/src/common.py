
from urlparse import urlparse
import woothee
import urllib

def DJBHash(key):
    # DJB Hash algorithm
    hash = 5381
    for i in range(len(key)):
        hash = ((hash <<5) + hash) + ord(key[i])

    return ( (hash & 0x7FFFFFFF))

alexa_top_million = []
f = open('../data/top-1m.csv')
for line in f:
    alexa_top_million.append(DJBHash( line.split(',')[1][:-1]))

alexa_top_million_hashed = set(alexa_top_million)

def parse_log_line(log_line):
    #Trim whitespace
    log_line = log_line.strip(' ')
    log_line = log_line.split(' ')
    line_array = []
    for x in log_line:
        if len(x) > 0:
            line_array.append(x)

    return line_array

def get_alexa_top_million(host):

    try:
        host_terms = host.split('.')
        host_last_two_hashed =  DJBHash( '.'.join(host_terms[-2:]) )

        if host_last_two_hashed in alexa_top_million_hashed:
            return 1
        else:
            return 0
    except:
        return 0

def get_status(s):
    if s == 'true':
        return 1
    else:
        return 0

def get_scheme(s):
    if s == 'https':
        return 2
    elif s == 'http':
        return 1
    else:
        return 0

def get_hostname(h):

    if h is not None:
        if h == 'faceboook.com':
            return 1
        else:
            return 2
    else:
        return 0

def get_os_family(os):
    if 'windows' in os:
        return 1
    elif os == 'bsd':
        return 2
    elif 'mac' in os:
        return 3
    elif os == 'linux':
        return 4
    elif os == 'unknown':
        return 0
    else:
        return 0

def get_version(v):
    if 'unknown' in v:
        return 0
    elif len(v) > 0:
        return 1
    else:
        return 0

def get_os_version(v):
    if 'unknown' in v:
        return 0 #'unknown'
    elif '10' in v:
        return 1 #'10.x'
    elif 'amd64' in v:
        return 2 #'amd64'
    elif 'nt' in v:
        return 3 #'nt'
    else:
        return 0

def get_category(c):
    if c == 'unknown':
        return 0
    elif c == 'crawler':
        return 1
    elif c == 'pc':
        return 2
    else:
        return 0

def get_vendor(v):
    if v == 'apple':
        return 1
    elif v == 'microsoft':
        return 2
    elif v == 'mozilla':
        return 3
    else:
        return 0

def get_name(name):
    if name == 'firefox':
        return 1
    elif 'explorer' in name:
        return 2
    elif 'crawler' in name:
        return 3
    elif name == 'safari':
        return 4
    elif name == 'unknown':
        return 0
    else:
        return 0


def extract_features_from_log(line, source):

    if source == 'training_data':
        assert len(line) == 4
        status=(get_status( line[3].split('\n')[0]))

    elif source == 'live_data':
        assert len(line) == 3

    # Parse IP
    ip=(line[0])
    j = ip.split('.')
    ip_1 = int(j[0])
    ip_2 = int(j[1])
    ip_3 = int(j[2])
    ip_4 = int(j[3])

    # Parse User Agent
    user_agent=( urllib.unquote(line[1]) )

    p = woothee.parse(user_agent.replace('+',' '))
    category = get_category ( p['category'].lower())
    os_version = get_os_version( p['os_version'].lower() )
    vendor = get_vendor( p['vendor'].lower())
    name = get_name( p['name'].lower())
    os = get_os_family( p['os'].lower())
    version = get_version(p['version'].lower())

    # Parse Referer
    referer=( urllib.unquote(line[2]) )
    p = urlparse(referer)
    scheme= get_scheme( p.scheme)
    hostname = get_hostname( p.hostname)
    alexa_top_million = get_alexa_top_million(p.hostname)
    len_path = len( p.path)
    len_query = len(p.query)
    len_host = str(p.hostname).count('.')

    if source == 'training_data':
        return [ip_1, ip_2, ip_3, ip_4, category, os_version, version, vendor, name, os,
                        scheme, hostname, alexa_top_million, len_path, len_query, len_host, status]
    elif source == 'live_data':
        return [ip_1, ip_2, ip_3, ip_4, category, os_version, version, vendor, name, os,
                    scheme, hostname, alexa_top_million, len_path, len_query, len_host]
