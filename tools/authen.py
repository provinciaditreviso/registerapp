#!/usr/bin/env python
import sys
import os
from getopt import getopt
from getopt import GetoptError

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

if user == "antani" and password == "giubbotto":
	print "Access-Accept"
	sys.exit(0)
else:
	print "Access-Reject"
	sys.exit(1)
