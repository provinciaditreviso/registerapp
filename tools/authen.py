#!/usr/bin/env python
import sys
import os
from getopt import getopt
from getopt import GetoptError
import sqlite3
from hashlib import sha1

def authenticate(user,password):
	conn = sqlite3.connect('/var/www/cgi-bin/users.db')
	c = conn.cursor()
	c.execute('SELECT 1 FROM users WHERE number = ? and password = ?', (user,sha1(password).hexdigest()))
	if c.rowcount == 1:
		return True
	else:
		return False



try:
	optlist, args = getopt(sys.argv[1:],'u:p:')
except GetoptError as err:
	print "Valid options are only -u and -p" 
	sys.exit(2)

user = ''
password = ''
for argument in optlist:
	if argument[0]=='-u':
		user = argument[1]
	if argument[0]=='-p':
		password = argument[1]

if authenticate(user,password):
	print "Access-Accept"
	sys.exit(0)
else:
	print "Access-Reject"
	sys.exit(1)
