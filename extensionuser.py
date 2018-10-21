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
("alberto.bartocci",""),
("alberto.bianco",""),
("alessandro.cardellino",""),
("alessandro.torre",""),
("alfredo.marengo",""),
("alice.forin",""),
("andrea.ferrero",""),
("andrea.sattamino",""),
("andrea.tarabbo",""),
("andrea.viberti",""),
("angelo.cantamessa",""),
("anna.lusso",""),
("anna.serafino",""),
("annunziata.apicella",""),
("antonella.costa",""),
("antonella.ferrero",""),
("antonella.torchia",""),
("arianna.turco",""),
("bernardino.balocco",""),
("bruno.bosio",""),
("bruno.camera",""),
("bruno.capello",""),
("carla.cogno",""),
("carmela.ambrosino",""),
("cecilia.sorli",""),
("cesare.amerio",""),
("chiara.guzzon",""),
("cinzia.cassina",""),
("cinzia.mo",""),
("claudia.ferrando",""),
("claudio.geuna",""),
("cristiano.morone",""),
("davide.maestri",""),
("denisa.ujhelyiova",""),
("diego.casavecchia",""),
("domenico.manissero",""),
("elena.bosca",""),
("elio.sorba",""),
("elisa.roati",""),
("elisa.savoia",""),
("eloisa.chille",""),
("emanuela.borsa",""),
("emanuela.pavanello",""),
("enrico.bellini",""),
("faruk.hadzimahmutovic",""),
("federica.bosco",""),
("francesca.gambino",""),
("francesca.reggio",""),
("Gabriella.brasca",""),
("gianfranco.giordano",""),
("gianfranco.giordano",""),
("gianluigi.renzi",""),
("gianni.zanchettin",""),
("giorgio.prasso",""),
("giovanni.lurgo",""),
("giulia.desalvia",""),
("giuliana.borsa",""),
("giuliano.d'errico",""),
("ilaria.tortone",""),
("katia.montemarano",""),
("katrin.frere",""),
("krystyna.lotarska",""),
("luca.romagnolo",""),
("luciana.surra",""),
("luciano.ruella",""),
("luigi.dirago",""),
("manlio.ghione",""),
("marco.brunetto",""),
("maria.gambaudo",""),
("marina.cocino",""),
("marinella.stella",""),
("massimo.canta",""),
("massimo.rivella",""),
("massimo.roero",""),
("matteo.restagno",""),
("maurizio.dimaria",""),
("mauro.nebbia",""),
("mauro.pelassa",""),
("mauro.ruatasio",""),
("michele.filipponi",""),
("mimmo.criscione",""),
("natalino.bona",""),
("paola.daddato",""),
("paola.garbarino",""),
("paola.garbarino2",""),
("paolo.bordino",""),
("paolo.fuga",""),
("paolo.mainerdo",""),
("paolo.spola",""),
("pasquale.mossa",""),
("patricia.falciglia",""),
("patrizia.franceschini",""),
("piera.goffi",""),
("pierluigi.cassinelli",""),
("pierpaolo.masoero",""),
("portineria.valtanaro",""),
("reception",""),
("reparto.carta",""),
("riccardo.biasion",""),
("roberto.gallino",""),
("romano.bonino",""),
("rosangela.gioetto",""),
("sabine.pohl",""),
("sabrina.gamba",""),
("sante.sandron",""),
("sara.sorba",""),
("serenella.degasperin",""),
("silvia.cravero",""),
("simona.capozzolo",""),
("simona.delmondo",""),
("stefania.calorio",""),
("stefania.dogliotti",""),
("stefano.careglio",""),
("stefano.careglio",""),
("stefano.occhetti",""),
("stefano.racca",""),
("teodora.depina",""),
("tiziana.taretto",""),
("tiziano.rusin",""),
("traslo.salmoiraghi",""),
("vanda.carbone",""),
("veronica.mule",""),
("vito.mola","")
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


