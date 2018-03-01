""" Edit line forward

Generate DNs and associate them to usernames based on telephonenumber field in End User


This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import sys
import requests
from requests.auth import HTTPBasicAuth
from zeep import Client
from zeep.transports import Transport
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

###############DATI DA COMPLETARE
USER = "username"
PASSWORD = "password"
IP = "10.20.30.40"
VERSION = "11.5"
#fkuniversalLineTemplate = "d78e1398-a65c-b1f6-48d1-913c8a8901f5"
#################################



SESSION = requests.Session()
SESSION.verify = False
SESSION.auth = HTTPBasicAuth(USER, PASSWORD)
TRANSPORT = Transport(session=SESSION)
CLIENT = Client(
    'file:///usr/var/axlsqltoolkit/schema/'+VERSION+'/AXLAPI.wsdl',
    transport=TRANSPORT)

SERVICE = CLIENT.create_service("{http://www.cisco.com/AXLAPIService/}AXLAPIBinding",
                                "https://"+IP+"/axl/")

LOGIN = {
    "appNav":"ccmadmin",
    "j_username":USER,
    "j_password":PASSWORD
}

def main():
    """ Main function, associate call forward data from CSV to DNs """
    print("Insert comma-separated enduser list")
    userlist = sys.stdin.readline().rstrip().split(",")


    print("Insert Universal Line Template pkid")
    fkuniversallinetamplate = sys.stdin.readline().rstrip()

    ###LOGIN TO CUCM
    print("Logging in...")
    session = requests.Session()
    session.get("https://"+IP+"/ccmadmin/showHome.do", verify=False)
    session.post("https://"+IP+"/ccmadmin/j_security_check", LOGIN, verify=False)
    session.get("https://"+IP+"/ccmadmin/showHome.do", verify=False)

    print("Success!")

    errors = []
    increment = 1
    print("Line association in progress...")

    for i in userlist:
        print("\rUser "+str(increment)+"/"+str(len(userlist)), end="")
        increment = increment + 1
        #Find user pkid
        try:
            userdata = SERVICE.getUser(userid=i)["return"]["user"]
        except:
            errors.append(i)
            continue
        fkenduser = userdata["uuid"][1:-1].lower()
        usertelephonenumber = userdata["telephoneNumber"]
        #Check line does not exist
        result = SERVICE.listLine({"pattern":usertelephonenumber}, {})
        if result["return"] is None:
            #Create new DN and find pkid
            newdn = {"dnorpattern":usertelephonenumber,
                     "universallinetemplate":fkuniversallinetamplate}
            fknumplan = session.post("https://"+IP+"/ucmadmin/directorynumber/addDn/",
                                     json=newdn).text
            # Associate DN to enduser
            query = ("insert into endusernumplanmap (fkenduser,fknumplan,tkdnusage,sortorder) "
                     "VALUES ('"+fkenduser+"','"+fknumplan+"','1','0')")
            result = SERVICE.executeSQLUpdate(sql=query)
            if result["return"]["rowsUpdated"] != 1:
                errors.append(i)
        else:
            errors.append(i)


    if len(errors) > 0:
        print("\n\nUsers with errors::")
        for user in errors:
            print(user)
    else:
        print("Everything done")


if __name__ == '__main__':
    main()
