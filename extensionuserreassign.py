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
client = Client(    'file:///mnt/c/Users/Operatore/Downloads/axlsqltoolkit/schema/'+version+'/AXLAPI.wsdl',    transport=transport)

service = client.create_service("{http://www.cisco.com/AXLAPIService/}AXLAPIBinding","https://"+ip+"/axl/")

login = {
"appNav":"ccmadmin",
"j_username":user,
"j_password":password
}

print("Inserire lista username separati da virgola")
userlist = [
("3288",""),
("3152",""),
("3460",""),
("3207",""),
("3470",""),
("3201",""),
("3060",""),
("3473",""),
("3869",""),
("3351",""),
("3117",""),
("3673",""),
("3175",""),
("3315",""),
("3130",""),
("3168",""),
("3089",""),
("3251",""),
("3304",""),
("3376",""),
("3462",""),
("3364",""),
("3296",""),
("3290",""),
("3248",""),
("3406",""),
("3476",""),
("3196",""),
("3190",""),
("3337",""),
("3162",""),
("3253",""),
("3265",""),
("3418",""),
("3396",""),
("3494",""),
("3338",""),
("8236",""),
("3023",""),
("3074",""),
("6306821",""),
("3662",""),
("3929",""),
("3421",""),
("3329",""),
("3197",""),
("3440",""),
("3667",""),
("3209",""),
("3229",""),
("6306899",""),
("3092",""),
("3120",""),
("3234",""),
("3126",""),
("3403",""),
("3402",""),
("3491",""),
("3439",""),
("3291",""),
("3870",""),
("3097",""),
("3169",""),
("3266",""),
("3281",""),
("3020",""),
("3412",""),
("3061",""),
("3277",""),
("3991",""),
("3078",""),
("3088",""),
("3109",""),
("3641",""),
("3391",""),
("3346",""),
("3128",""),
("3232",""),
("3477",""),
("3200",""),
("3646",""),
("3640",""),
("3677",""),
("3437",""),
("3689",""),
("3219",""),
("3490",""),
("3096",""),
("3411",""),
("3028",""),
("3255",""),
("3238",""),
("3685",""),
("3695",""),
("3189",""),
("3427",""),
("3392",""),
("3883",""),
("3691",""),
("3116",""),
("3424",""),
("3472",""),
("3250",""),
("3051",""),
("3362",""),
("3344",""),
("3280",""),
("3285",""),
("3244",""),
("3036",""),
("3256",""),
("3225",""),
("3693",""),
("3124",""),
("3339",""),
("3050",""),
("3497",""),
("3264",""),
("3247","")
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
	print("\rUtente "+str(increment)+"/"+str(len(userlist)),end="")
	increment = increment + 1
	#Find user pkid
	try:
		userdata = service.getUser(userid=i[0])["return"]["user"]
	except:
		errors.append(i)
		continue
	fkenduser = userdata["uuid"][1:-1].lower()
	#Create new DN and find pkid
	devicename = (userdata["lastName"]+userdata["firstName"]).upper()
	devicejson = {"tkproduct":"509","tkdeviceprotocol":"11","name":"SEP"+devicename,"fkcommondevicetemplate":"55972bd6-1897-8062-9862-b5978b8b172e","isprofile":"t","moduleCount":0}
	associateDo = s.post("https://"+ip+"/ucmadmin/enduser/addPhone/"+fkenduser,json=devicejson).text



if len(errors) > 0:
	print("\n\nUtenti non caricati correttamente:")
	for user in errors:
		print(user)
else:
	print("TUTTAPPOSTO DOTTO'")


