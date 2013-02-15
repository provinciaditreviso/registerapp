#!/usr/bin/env python
import sqlite3
import string
import random
import cgi
import re
from datetime import datetime
from hashlib import sha1
from tempfile import mkstemp
import os


def pwgen(size):
	return ''.join([random.choice([l for l in (string.letters+string.digits)]) for i in range(size)])

def register(number):
	if re.match("^3[0-9]{8,9}$",number):
		conn = sqlite3.connect('users.db')
		c = conn.cursor()
		password = pwgen(8)
		data = (number,sha1(password).hexdigest(),datetime.now().isoformat())
		try:
			c.execute("INSERT INTO users VALUES (?,?,?)",data)
			conn.commit()
		except sqlite3.IntegrityError:
			# element already in the database
			return 1
		sms = "To: "+number+"\n\n Servizio WIFI Provincia di Treviso - Utente: "+number+" Password: "+password
		#fdsms, fsms = mkstemp(prefix="sms-",dir="/var/spool/sms/outgoing/")
		fdsms, fsms = mkstemp(prefix="sms-",dir="/tmp/")
		outf=os.fdopen(fdsms,'wt')
		outf.write(sms)
		outf.close()
		return 0
	else:
		return 2

def change(number):
	if re.match("^3[0-9]{8,9}$",number):
		conn = sqlite3.connect('users.db')
		c = conn.cursor()
		c.execute("SELECT 1 FROM users WHERE number = ?",(number,))
		if len(c.fetchall()) == 1:
			password = pwgen(8)
			c.execute("UPDATE users SET password = ? WHERE number = ?",(password,number))
			conn.commit()
			sms = "To: "+number+"\n\n Servizio WIFI Provincia di Treviso - Nuova password per l'utente "+number+" Password: "+password
	                fdsms, fsms = mkstemp(prefix="sms-",dir="/tmp/")
	                #fdsms, fsms = mkstemp(prefix="sms-",dir="/var/spool/sms/outgoing/")
	                outf=os.fdopen(fdsms,'wt')
	                outf.write(sms)
	                outf.close()
			return 0
		else:
			return 1
	else:
		return 2


print "Content-Type: text/html\n\n"

form = cgi.FieldStorage()
if form.has_key("number") and form.has_key("action"):
		if form["action"].value == "newpassword":
			retv = change(form["number"].value)
			if retv == 0:
				print "SMS Inviato con la nuova password\n"
			elif retv == 1:
				print "Utente non ancora registrato"				
			elif retv == 2:
				print "Numero errato"
		elif form["action"].value == "newuser":
			retv = register(form["number"].value)
			if retv == 0:
				print "SMS Inviato con le credenziali\n"
			elif retv == 1:
				print "Utente gia' registrato"				
			elif retv == 2:
				print "Numero errato"

		else:
			print "Invalid choice"
else:
	print "Some parameters are missing"
