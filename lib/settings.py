import threading
from lib.objects import *
import sqlite3 as lite
import redis
import json


def get_top_domains(dbname):
    con = lite.connect(dbname)
    con.text_factory = str
    with con:
        cur = con.cursor()
        cur.execute("SELECT domain FROM domains")
        rows = cur.fetchall()
        domains = []
        if rows:
            for row in rows:
                domains.append(row[0])
        else:
            pass
        return domains


# Verify Redis objects and create if needed
r = redis.Redis()
if r.exists('falcongate-main') == 0:
    r.hmset('falcongate-main', falcongate_main)

if r.exists('dhcp-hosts') == 0:
    r.hmset('dhcp-hosts', {'active': 1})

if r.exists('dhcp-history') == 0:
    r.hmset('dhcp-history', {'active': 1})

if r.exists('user-ip-blacklist') == 0:
    r.hmset('user-ip-blacklist', {'active': 1})

if r.exists('user-ip-whitelist') == 0:
    r.hmset('user-ip-whitelist', {'active': 1})

if r.exists('user-domain-blacklist') == 0:
    r.hmset('user-domain-blacklist', {'active': 1})

if r.exists('user-domain-whitelist') == 0:
    r.hmset('user-domain-whitelist', {'active': 1})

if r.exists('fg-intel-creds') == 0:
    r.hmset('fg-intel-creds', {'active': 1})

if r.exists('fg-intel-ip') == 0:
    r.hmset('fg-intel-ip', {'active': 1})

if r.exists('fg-intel-domain') == 0:
    r.hmset('fg-intel-domain', {'active': 1})

# Global variables
# Master network object
global homenet
homenet = Network()

# Master lock for threads
global lock
lock = threading.Lock()

# Master list of bad IP addresses
global bad_ips
bad_ips = []

# Master whitelist of IP addresses
global good_ips
good_ips = []

# Top domains whitelist
global top_domains
top_domains = get_top_domains("db/top_domains.sqlite")

# Master thread list
global threads
threads = {}

# Stats globals
global country_stats
country_stats = {}
for k in CC.keys():
    country_stats[k] = Country(k, CC[k])

global hosts_stats
hosts_stats = {}




