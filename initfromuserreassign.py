# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


import requests
from zeep import Client
from zeep.transports import Transport
from requests.auth import HTTPBasicAuth
import urllib3
import sys
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

###############DATI DA COMPLETARE
USER = "user"
PASSWORD = "password"
IP = "10.20.30.40"
VERSION = "11.5"
#################################



session = requests.Session()
session.verify = False
session.auth = HTTPBasicAuth(user, password)
transport = Transport(session=session)
client = Client(
    'file:///mnt/c/Users/Federico Tabbò/Downloads/axlsqltoolkit/schema/'+version+'/AXLAPI.wsdl',
    transport=transport)

service = client.create_service("{http://www.cisco.com/AXLAPIService/}AXLAPIBinding","https://"+ip+"/axl/")

login = {
"appNav":"ccmadmin",
"j_username":user,
"j_password":password
}

print("Inserire lista username separati da virgola")
userlist = sys.stdin.readline().rstrip().split(",")


###LOGIN TO CUCM
print("Logging in...")
s = requests.Session()
a = s.get("https://"+ip+"/ccmadmin/showHome.do",verify=False)
a = s.post("https://"+ip+"/ccmadmin/j_security_check",login,verify=False)
a = s.get("https://"+ip+"/ccmadmin/showHome.do",verify=False)

print("Success!")


errors = []
increment = 1
print("Associazione linee")

for i in userlist:
	print("\rUtente "+str(increment)+"/"+str(len(userlist)),end="")
	increment = increment + 1
	#Find user pkid
	try:
		userdata = service.getUser(userid=i)["return"]["user"]
		print(userdata)
		fknumplan = service.getDn(routePartitionName="PT-NOT-YET-MIGRATED",pattern=i)["return"]
		print(fknumplan)
	except:
		errors.append(i)
		continue
	fkenduser = userdata["uuid"][1:-1].lower()
	userTelephoneNumber = userdata["telephoneNumber"]
	#Check line does not exist
	result = service.listLine({"pattern":userTelephoneNumber},{})
	print(fkenduser)
	print(fknumplan)
	if result["return"] is not None:
		query = "insert into endusernumplanmap (fkenduser,fknumplan,tkdnusage,sortorder) VALUES ('"+fkenduser+"','"+fknumplan+"','1','0')"
		result = service.executeSQLUpdate(sql=query)
		if result["return"]["rowsUpdated"] != 1:
			errors.append(i)
	else:
		errors.append(i)


if len(errors) > 0:
	print("\n\nUtenti non caricati correttamente:")
	for user in errors:
		print(user)
else:
	print("TUTTAPPOSTO")