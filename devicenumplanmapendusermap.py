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
client = Client('file:///mnt/c/Users/Operatore/Downloads/axlsqltoolkit/schema/'+version+'/AXLAPI.wsdl',transport=transport)

service = client.create_service("{http://www.cisco.com/AXLAPIService/}AXLAPIBinding","https://"+ip+"/axl/")


listUser = service.listUser(searchCriteria={"userid":"federico.tabbo"},returnedTags=())["return"]["user"]

for endUser in listUser:
	curUser = service.getUser(uuid=endUser["uuid"])["return"]["user"]
	print(curUser)
	priExtensionPattern = curUser["primaryExtension"]["pattern"]
	priExtensionRoutePartition = curUser["primaryExtension"]["routePartitionName"]
	print(priExtensionPattern)
	print("------------")
	curDN = service.getLine(pattern=priExtensionPattern,routePartitionName=priExtensionRoutePartition)["return"]["line"]
	curDNpkid = curDN["uuid"][1:-1]
	curDNassociatedDevices = curDN["associatedDevices"]["device"]

	for phone in curDNassociatedDevices:
		curPhone = service.getPhone(name=phone)["return"]["phone"]
		print(curPhone["name"])
		curPhoneLines = curPhone["lines"]

		print("---------")
		print(curPhoneLines["line"][0])
		print("----------")

		for line in curPhoneLines["line"]:
			print("FOR LOOP")
			print("LINE")
			print(line)
			print("PRIEXTENSION")
			print(priExtensionPattern)
			if int(line["dirn"]["pattern"]) == int(priExtensionPattern):
				rightLine = curPhoneLines["index"]

		service.updatePhone(name=phone,lines={"line":{"index":rightLine,"dirn":{"pattern":priExtensionPattern,"routePartitionName":priExtensionRoutePartition},"associatedEndusers":{"enduser":{"userId":curUser}}}})