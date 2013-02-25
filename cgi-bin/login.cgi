#!/usr/bin/env python

import os
import sys
import cgi
from hashlib import md5
from struct import pack
from binascii import hexlify, unhexlify


# Set of Global Variables
UAMSECRET = "1234567890"
USERPASSWORD = 1
LOGINPATH = os.getenv('SCRIPT_NAME','/cgi-bin/login.cgi')
CHILLISPOT = "Hotspot"
TITLE = CHILLISPOT + " Login"
CENTERUSERNAME = "Utente"
CENTERPASSWORD = "Password"
CENTERLOGIN = "Login"
CENTERPLEASEWAIT = "Attendere...."
CENTERLOGOUT = "Disconnetti"
H1LOGIN = CHILLISPOT + " Login"
H1FAILED = "Autenticazione fallita"
H1LOGGEDIN = "Autenticato con "+CHILLISPOT
H1LOGGINGIN = "Autenticazione in corso..."
H1LOGGEDOUT = "Disconnesso da "+CHILLISPOT
CENTERDAEMON = "Login deve essere effettuato attraverso il servizio "+CHILLISPOT
CENTERENCRYPTED = "Login deve essere effettuato su una connessione cifrata"


HEADER = open('/var/www/login/header_c.html').read()
FOOTER = open('/var/www/login/footer_c.html').read()


if False and os.getenv('HTTPS','') != 'on':
	print "Content-Type: text-html\n\n"
	print HEADER
	print "<div class=\"page-header\"><h1>%s</h1></div><p class=\"lead\">%s</p>" % ( H1FAILED, CENTERENCRYPTED )
	print FOOTER
	print """<!--
	<?xml version=\"1.0\" encoding=\"UTF-8\"?>
	<WISPAccessGatewayParam
	 xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\"
	 xsi:noNamespaceSchemaLocation=\"http://www.acmewisp.com/WISPAccessGatewayParam.xsd\">
		<AuthenticationReply>
			<MessageType>120</MessageType>
			<ResponseCode>102</ResponseCode>
			<ReplyMessage>Login must use encrypted connection</ReplyMessage>
		</AuthenticationReply>
	</WISPAccessGatewayParam>
	-->"""
	print "</html>"
	sys.exit(0)

form = cgi.FieldStorage()
if form.has_key('UserName'):
	username = form['UserName'].value
if form.has_key('Password'):
	password = form['Password'].value
if form.has_key('challenge'):
	challenge = form['challenge'].value
if form.has_key('button'):
	button = form['button'].value
else:
	button = ''
if form.has_key('logout'):
	logout = form['logout'].value
if form.has_key('prelogin'):
	prelogin = form['prelogin'].value
if form.has_key('res'):
	res = form['res'].value
if form.has_key('uamip'):
	uamip = form['uamip'].value
if form.has_key('uamport'):
	uamport = form['uamport'].value
if form.has_key('userurl'):
	userurl = form['userurl'].value
else:
	userurl = ''
if form.has_key('timeleft'):
	timeleft = form['timeleft'].value
else:
	timeleft = ''
if form.has_key('redirurl'):
	redirurl = form['redirurl'].value
else:
	redirurl = ''
if form.has_key('reply'):
	reply = form['reply'].value

if button == 'Login':
	hexchal = unhexlify(challenge)
	if len(UAMSECRET) > 0:
		newchal = md5(hexchal + UAMSECRET).digest()
	else:
		newchal = hexchal
	response = md5("\0" + password + newchal).hexdigest()
	newpwd = password[:32]
	pappassword =  "".join(hexlify(newpwd ^ newchal))
	
	if len(UAMSECRET)>0 and USERPASSWORD == 1:
		
		url = "http://"+uamip+":"+uamport+"/logon?username="+username+"&password="+pappassword+"\">"
	else:
		url = "http://"+uamip+":"+uamport+"/logon?username="+username+"&response="+response+"&userurl="+userurl+"\">"
	
	print "Content-type: text/html\n\n"
	print """
		<html>
		<head>
		<meta http-equiv=\"Cache-control\" content=\"no-cache\">
		<meta http-equiv=\"Pragma\" content=\"no-cache\">
		<meta http-equiv=\"refresh\" content=\"0;url=%s\">
		</head>
		<body>
		<center>
		%s
		</center>
		</body>
		<!--
		 <WISPAccessGatewayParam 
			xmlns:xsi=\"http://www.w3.org/2001/XMLSchema-instance\" 
			xsi:noNamespaceSchemaLocation=\"http://www.acmewisp.com/WISPAccessGatewayParam.xsd\">
			<AuthenticationReply> 
			<MessageType>120</MessageType>
			<ResponseCode>201</ResponseCode>
			<LoginResultsURL>%s</LoginResultsURL>
			</AuthenticationReply>
		</WISPAccessGatewayParam>
		-->
		</html>
	""" % (url, CENTERPLEASEWAIT,url)	

	system.exit(0)


switch = { 'success': 1, 'failed': 2, 'logoff': 3, 'already': 4, 'notyet': 5, 'smartclient': 6, 'popup1': 11, 'popup2': 12, 'popup3': 13 }

if switch.has_key(res):
	result = switch[res]
else:
	result = 0

if result == 0:
	print "Content-type: text/html\n\n"
	print HEADER
	print """
		<div class=\"page-header\"<h1>%s</h1></div>
		<p class=\"lead\">
			%s
		</p>
	""" % (TITLE,CENTERDAEMON)
	print FOOTER
	print "</html>"	
	print str(res)
	sys.exit(0)

print open('/var/www/login/header_m.html').read().format(LOGINPATH,uamip,uamport,result,LOGINPATH,uamip,uamport,userurl,redirurl,timeleft,userurl,redirurl,timeleft,result)


if result == 2:
	print "<div class=\"page-header\"><h1>%s</h1></div>" % (H1FAILED)
	if reply:
		print "<p class=\"lead\">%s</p>" % (reply)

if result == 5:
   print """
  	<div class=\"page-header\"><h1>%s</h1></div>
	""" % (H1LOGIN)

if result == 2 or result == 5:
	print """
	  <p><form class ="form-signin" name=\"form1\" method=\"post\" action=\"%s\">
	  <h2 class=\"form-signin-heading\">Autenticazione:</h2>
	  <input type=\"hidden\" name=\"challenge\" value=\"%s\">
	  <input type=\"hidden\" name=\"uamip\" value=\"%s\">
	  <input type=\"hidden\" name=\"uamport\" value=\"%s\">
	  <input type=\"hidden\" name=\"userurl\" value=\"%s\">
	  <input class=\"input-block-level\" type=\"text\" name=\"UserName\" placeholder=\"%s\" size=\"20\" maxlength=\"128\" />
	  <input class=\"input-block-level\" type=\"password\" name=\"Password\" placeholder=\"%s\" size=\"20\" maxlength=\"128\"></td>
	  <button class=\"btn btn-large btn-primary\" type=\"submit\" name=\"button\" value=\"Login\" onClick=\"javascript:popUp('%s?res=popup1&uamip=%s&uamport=%s')\">Login</button> 
	  </form></p>""" % (LOGINPATH,challenge,uamip,uamport,userurl,CENTERUSERNAME,CENTERPASSWORD,LOGINPATH,uamip,uamport)

if result == 1:
  print "<div class=\"page-header\"><h1>%s</h1></div>" % (H1LOGGEDIN)

  if reply: 
     print "<p class=\"lead\">%s</p>" % (reply)

  print """
  <p>
    <a href=\"http://%s:%s/logoff\">Logout</a>
  </p>
	""" % (uamip,uamport)

if result == 4 or result == 12:
	print """
	<div class=\"page-header\"><h1>%s</h1></div>
	<p class=\"lead\">
	   <a href=\"http://%s:%s/logoff\">%s</a>
	</p>
	""" % (H1LOGGEDIN,uamip,uamport,CENTERLOGOUT)


if result == 11:
	print """
	  <div class=\"page-header\"><h1>%s</h1></div>
	  <p class=\"lead\">
	    %s
	  </p>
	""" % (H1LOGGINGIN,CENTERPLEASEWAIT)



if result == 3 or result == 13:
	  print """
	  <div class=\"page-header\"><h1>%s</h1></div>
	  <p class=\"lead\">
	    <a href=\"http://%s:%s/prelogin\">%s</a>
	  </p>
		""" % (H1LOGGEDOUT,uamip,uamport,CENTERLOGIN)

print FOOTER

sys.exit(0)	
