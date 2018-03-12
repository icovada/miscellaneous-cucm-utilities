""" Edit line forward

Edit DNs in CSV updating line CSS.

Accepts CSV input as file "linecss.csv" in the same folder, with header
dn,partition,shareLineAppearanceCssName

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

import csv
import requests
from requests.auth import HTTPBasicAuth
from zeep import Client
from zeep.transports import Transport
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


###############Data to fill in
USER = "user"
PASSWORD = "password"
IP = "10.20.30.40"
VERSION = "11.5"
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


def main():
    """ Main function, associate call forward data from CSV to DNs """
    errors = []
    increment = 1

    with open("linecss.csv", "r") as theinput:
        reader = csv.DictReader(theinput)
        for line in reader:
            print("\rUtente "+str(increment), end="")
            increment = increment + 1
            #Find user pkid
            try:
                SERVICE.updateLine(pattern=line["dn"],
                                   routePartitionName=line["partition"],
                                   shareLineAppearanceCssName=line["shareLineAppearanceCssName"]
                                  )
            except:
                errors.append(line["dn"])
                continue

    if len(errors) > 0:
        print("\n\nUsers with errors:")
        for user in errors:
            print(user)
    else:
        print("Everything done")


if __name__ == '__main__':
    main()
