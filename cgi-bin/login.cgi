#!/usr/bin/env python

import os
import sys
import cgi
from struct import pack
from binascii import hexlify, unhexlify


# Set of Global Variables
UAMSECRET = "bababababababababaab"
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


HEADER = ""
FOOTER = ""


if os.getenv('HTTPS','') != 'on':
	print "Content-Type: text-html\n\n"
	print HEADER
	print "<h1>%s</h1> <center>%s</center>" % ( H1FAILED, CENTERENCRYPTED )
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
	username = form['UserName']
if form.has_key('Password'):
	password = form['Password']
if form.has_key('challenge'):
	challenge = form['challenge']
if form.has_key('button'):
	button = form['button']
if form.has_key('logout'):
	logout = form['logout']
if form.has_key('prelogin'):
	prelogin = form['prelogin']
if form.has_key('res'):
	res = form['res']
if form.has_key('uamip'):
	uamip = form['uamip']
if form.has_key('uamport'):
	uamport = form['uamport']
if form.has_key('userurl'):
	userurl = form['userurl']
if form.has_key('timeleft'):
	timeleft = form['timeleft']
if form.has_key('redirurl'):
	redirurl = form['redirurl']
if form.has_key('reply'):
	reply = form['reply']

if button == 'Login':
	hexchal = unhexlify(challenge)
	if len(UAMSECRET) > 0:
		newchal = md5(hexchal+uamsecret).digest()
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
	result = switch(res)
else:
	result = 0

if result == 0:
	print "Content-type: text/html\n\n"
	print HEADER
	print """
		<h1>%s</h1>
		<center>
			%s
		</center>
	"""
	print FOOTER
	print "</html>"	
	sys.exit(0)

print HEADER
print BODY

if result == 2:
	print "<h1 style=\"text-align: center;\">%s</h1>" % (H1FAILED)
	if reply:
		print "<center>%s </BR></BR></center>" % (reply)

if ($result == 5) {
   print """
  <h1 style=\"text-align: center;\">$h1Login</h1>";
  """

if ($result == 2 || $result == 5) {
  print """
  <form name=\"form1\" method=\"post\" action=\"$loginpath\">
  <input type=\"hidden\" name=\"challenge\" value=\"$challenge\">
  <input type=\"hidden\" name=\"uamip\" value=\"$uamip\">
  <input type=\"hidden\" name=\"uamport\" value=\"$uamport\">
  <input type=\"hidden\" name=\"userurl\" value=\"$userurl\">
  <center>
  <table border=\"0\" cellpadding=\"5\" cellspacing=\"0\" style=\"width: 217px;\">
    <tbody>
      <tr>
        <td align=\"right\">$centerUsername:</td>
        <td><input style=\"font-family: Arial\" type=\"text\" name=\"UserName\" size=\"20\" maxlength=\"128\"></td>
      </tr>
      <tr>
        <td align=\"right\">$centerPassword:</td>
        <td><input style=\"font-family: Arial\" type=\"password\" name=\"Password\" size=\"20\" maxlength=\"128\"></td>
      </tr>
      <tr>
        <td align=\"center\" colspan=\"2\" height=\"23\"><input type=\"submit\" name=\"button\" value=\"Login\" onClick=\"javascript:popUp('$loginpath?res=popup1&uamip=$uamip&uamport=$uamport')\"></td> 
      </tr>
    </tbody>
  </table>
  </center>
  </form>"""

if ($result == 1) {
  echo "
  <h1 style=\"text-align: center;\">$h1Loggedin</h1>";

  if ($reply) { 
      echo "<center> $reply </br></br></center>";
  }

  echo "
  <center>
    <a href=\"http://$uamip:$uamport/logoff\">Logout</a>
  </center>
</body>
</html>";
}

if (($result == 4) || ($result == 12)) {
  echo "
  <h1 style=\"text-align: center;\">$h1Loggedin</h1>
  <center>
    <a href=\"http://$uamip:$uamport/logoff\">$centerLogout</a>
  </center>
</body>
</html>";
}


if ($result == 11) {
  echo "
  <h1 style=\"text-align: center;\">$h1Loggingin</h1>
  <center>
    $centerPleasewait
  </center>
</body>
</html>";
}


if (($result == 3) || ($result == 13)) {
  echo "
  <h1 style=\"text-align: center;\">$h1Loggedout</h1>
  <center>
    <a href=\"http://$uamip:$uamport/prelogin\">$centerLogin</a>
  </center>
</body>
</html>";
}

exit(0);	
