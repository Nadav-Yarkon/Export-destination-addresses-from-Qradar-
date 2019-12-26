########Export destinations addresses from the offense in Qradar ########
########### Author: Nadav Yarkon #############
    ### For Educational Purposes Only ###

#Author: Nadav Yarkon
#Email: Nadavy2469 @ gmail.com
#https: https://github.com/Nadav-Yarkon

import urllib3
import requests
import argparse
import json
import time

urllib3.disable_warnings()

class GetIpFromQradar:

    def __init__(self, AQL):
        self.AQL = AQL
        self.main()

    def main(self):
        ip = self.ParseDestination(self.ConnectToAPIwithSearchID(self.getSearchID()))
        self.WirteToFile(ip)


    def getSearchID(self):
        BASE_URL = "https://<IP of Qradar>/api/ariel/searches"
        headers = {
            'SEC': '<API KEY>'
        }
        url = BASE_URL + "?query_expression=" + self.AQL
        json_data = requests.post(url, headers=headers, verify=False).json()
        search_id = json_data['search_id']
        return search_id


    def ConnectToAPIwithSearchID(self,search_id):
        BASE_URL = 'https://<IP of Qradar>/api/ariel/searches/'+search_id+'/results'
        headers = {
            'SEC': '<API KEY>'
        }
        url = BASE_URL
        time.sleep(4)
        json_data = requests.get(url, headers=headers, verify=False).json()
        return json_data


    def ParseDestination(self,json_data):
        for ips in json_data.values():
            dstIP = list(set(val for dic in ips for val in dic.values()))
            return dstIP

    def WirteToFile(self,newarr):
        file = open("addresses.txt", 'w')
        for address in newarr:
            file.write(address+'\n')
        file.close()


parser = argparse.ArgumentParser(description='The program take all destination IP from offense (enter number of offansse) \n After send all destination to Virus total')
parser.add_argument("-i", "-id" , metavar='' , required=True , help= "ID of offensse from Qradar" , type=int)
parser.add_argument("-s", "-src" , metavar='' , help="Source IP , traffic from particular source IP" ,type=str)
parser.add_argument("-p", "-port" , metavar=''  , help="Port of traffic. traffic on a particular port" , type=int)
parser.parse_args()
args = parser.parse_args()

if args.s == None and args.p == None:
    AQL = "SELECT destinationip FROM events where INOFFENSE("+str(args.i)+") GROUP BY destinationip last 7 DAYS"
    GetIpFromQradar(AQL)
elif args.p is not None and args.s == None:
    AQL = "SELECT destinationip FROM events where INOFFENSE("+str(args.i)+") and destinationport = " + str(args.p) + " GROUP BY destinationip last 7 DAYS"
    GetIpFromQradar(AQL)
elif args.p == None and args.s is not None:
    AQL = "SELECT destinationip FROM events where INOFFENSE("+str(args.i)+") and sourceip = " + args.s + " GROUP BY destinationip last 7 DAYS"
    GetIpFromQradar(AQL)
elif not (args.p == None and args.s == None):
    AQL = "SELECT destinationip FROM events where INOFFENSE("+str(args.i)+") and destinationport = " + str(args.p) + " and sourceip = " + args.s +" GROUP BY destinationip last 7 DAYS"
    GetIpFromQradar(AQLs)
