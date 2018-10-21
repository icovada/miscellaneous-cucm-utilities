# coding=UTF-8

import requests
from zeep import Client
from zeep.transports import Transport
from requests.auth import HTTPBasicAuth
import sys


###############DATI DA COMPLETARE
USER = "user"
PASSWORD = "password"
IP = "10.20.30.40"
VERSION = "11.5"
#fkuniversalLineTemplate = "d78e1398-a65c-b1f6-48d1-913c8a8901f5"
#################################



session = requests.Session()
session.verify = False
session.auth = HTTPBasicAuth(user, password)
transport = Transport(session=session)
client = Client(    'file:///mnt/c/Users/Federico Tabbò/Downloads/axlsqltoolkit/schema/'+version+'/AXLAPI.wsdl',    transport=transport)

service = client.create_service("{http://www.cisco.com/AXLAPIService/}AXLAPIBinding","https://"+ip+"/axl/")

login = {
"appNav":"ccmadmin",
"j_username":user,
"j_password":password
}

print("Inserire lista username separati da virgola")
userlist = [
("govone.portineria","5dd0"),
("gianluigi.barberis","5d95"),
("emanuele.cianci","6069"),
("marcella.bernardini","5c87"),
("vincenzo.daniele","55e5"),
("laura.bianco","5553"),
("davide.solaro","566c"),
("fabrizio.sacco","6114"),
("paola.cogno","a0b9"),
("paola.cogno","64b0"),
("marco.albesano","521f"),
("gianni.masenta","624d"),
("marco.lano","52bc"),
("roberto.pisano","5473"),
("maurizio.carapezza","5213"),
("maurizio.carapezza","5266"),
("rosario.lauria","a1cb"),
("luigi.alberti","52db"),
("barbara.torta","a26a"),
("silvia.masucco","a14c"),
("assegnare numero nuovo","ced1"),
("luigi.macario","5269"),
("raimondo.rava","52a1"),
("bruno.boeris","52e2"),
("luigi.macario","cc47"),
("valeria.bella","5266"),
("mario.degiacomi","5d31"),
("sharon.reiso","543g"),
("elisa.giachino","526c"),
("claudio.marasso","5291"),
("infermeria","cce5"),
("robi.baracco","5338"),
("mauro.rivetti","52b8"),
("samuele.sarotto","524f"),
("dario.giamesio","7660"),
("claudia.castellino","6064"),
("claudio.cotto","5221")
]


###LOGIN TO CUCM
print("Logging in...")
s = requests.Session()
a = s.get("https://"+ip+"/ccmadmin/showHome.do",verify=False)
a = s.post("https://"+ip+"/ccmadmin/j_security_check",login,verify=False)
a = s.get("https://"+ip+"/ccmadmin/showHome.do",verify=False)

print("Success!")


errors = []
increment = 1
print("Associazione device")

for i in userlist:
	print("\rUtente "+str(increment)+"/"+str(len(userlist)))
	increment = increment + 1
	#Find user pkid
	try:
		userdata = service.getUser(userid=i[0])["return"]["user"]
	except:
		errors.append(i)
		continue
	deviceNameSearch = "SEP%" + i[1]
	fkenduser = userdata["uuid"][1:-1].lower()
	result = service.listPhone({"name":deviceNameSearch},{"name":""})
	if result["return"] == None:
		errors.append(i)
		print("result error")
		continue
	device = result["return"]["phone"]
	if len(device) == 1:
		fkdevice = device[0]["uuid"][1:-1].lower()
		#Create new DN and find pkid
		devicejson = {"devicelist":[{"pkid":fkdevice}]}
		associateDo = s.post("https://"+ip+"/ucmadmin/enduser/movePhones/"+fkenduser,json=devicejson).text
		if "error" in associateDo:
			errors.append(i)
			continue
	else:
		print("result len != 1")
		errors.append(i)


if len(errors) > 0:
	print("\n\nUtenti non caricati correttamente:")
	for user in errors:
		print(user)
else:
	print("TUTTAPPOSTO DOTTO'")


