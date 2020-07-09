# -*- coding: utf-8 -*-
"""
Created on Thu Jul  9 13:47:25 2020

@author: cpadmin
"""


import requests
import json
import time
# Create a file called creds.py that in not included in the repository so credentials are not exposed
from creds import *
import csv
from urllib.parse import urlparse


# Use BearerAuth class inline when authenticating to API 2. API1 used basic auth.
#_______________________________________________________________________________

class BearerAuth(requests.auth.AuthBase):
    def __init__(self, token):
        self.token = token
    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + self.token
        return r
#_______________________________________________________________________________
        
   
"""@Rakesh this def is obviously meant to have more code wrapped around it. In the UsrData variable for example, there are numerous varaibles
hardcoded. If they are in that varaible below, they are required. I would spend time reading the docs for optional vs required.
"""
# API 1 User Creation
def CreateUser(UsrE, UsrF, UsrL):
    UsrData = { "email" : UsrE, "FirstName" : UsrF, "LastName" : UsrL, "RoleID": "6", "Title": "CRM+ User", "EnterpirseHierarchy" : "16", "RegionID" : "1","CityID" : "14","CostCenterID" : "1" }
    header = {"content-type": "appilcation/json", "Accept": "text/plain"}
    NewUser = requests.post(url = instanceurl+apiendpoint,data=json.dumps(UsrData), headers=header, verify=False, auth=(username, jatoken))
    

# The below is obviously collecting variables from user input using another def, but the code after the ELSE: includes some example of how to 
# leverage the csv module to create csv files with the users in them
#USERS endpoint
def User():
    print ("From within the users endpoint, you can either retrieve all the users into a spreadsheet, or create a single user  \n")
    addUsr = input("Do you want to create a new user? [Y/N]:"+'\n') or "N"
    if (addUsr == "Y") or (addUsr == "y"):
        CollectUserInfo
        CreateUser(UsrEmail,UsrFN,UsrLN)
    else:
        print ("This script is now going to create a comma delimited file called userlist.csv in the same directory of this script with all of the users listed \n")   
        with open('userlist.csv', 'w', newline='') as myfile:
            out = csv.writer(myfile,dialect='excel',delimiter=',',quoting=csv.QUOTE_NONE,escapechar=' ')
            for eachUsr in usrArr:
                print(eachUsr)
                out.writerow([eachUsr])

# Just some user input examples if u want to see the mandatory fields needed to create a user
def CollectUserInfo():
    global UsrEmail
    UsrEmail = input("Please enter the full email address of the user [eg: ron.cavallo@cprime.com]")
    if not UsrEmail:
        UsrEmail = input("You must enter the full email address of the user [eg: ron.cavallo@cprime.com]")##This needs better checking 
    global UsrFN
    UsrFN = input("Please enter the full first name of the new user [eg: Jimeny]")
    if not UsrFN:
        UsrFN = input("You must enter the first name the user [eg: Jimeny]")
    global UsrLN
    UsrLN = input("Please enter the last name of the new user [eg: Cricket]")
    if not UsrLN:
        UsrFN = input("You must enter the last name the user [eg: Cricket]")
    return UsrEmail,UsrFN,UsrLN

def GetAllUsers():    
    global usrArr
    usrArr = []
    users = requests.get(instanceurl + "/users",  auth=BearerAuth(jatoken))
    data = users.json()
    for eachUsr in data:
        fn = eachUsr["firstName"]
        ln = eachUsr["lastName"]
        un = eachUsr['uid']
        em = eachUsr['email']
        usrArr.append(fn + ',' + ln + "," + un + ',' + em)
    return usrArr

# This collects all of the information about the server instance and api endpoint you want to work with and formats the url properly.
# This is the only place that the apiendpoint or the url should be manipulated or it breaks the rest of the routines that depend upon it.
def CollectApiInfo():
    global apiendpoint
    global instanceurl
    global api1instance
    apiendpoint = input("Enter the api endpoint for your instance in following format EG. ""cities"". It is very important that you spell this endpoint correctly. Please refer to the api documents E.G https://cprime.agilecraft.com/api-docs/public/ for the apiendpoints available : ")
    #print(apiendpoint)
    instanceurl = input("Enter the url for your instance in following format EG. ""https://cprime.agilecraft.com"" : ")
    ChkInput = input("Is this your correct instance and endpoint you want to work with?  " + instanceurl + " : " + apiendpoint + "  " + "\n")
    if (ChkInput == "N") or (ChkInput == "n"):
       CollectApiInfo()
    instanceurl = instanceurl + "/rest/align/api/2" ##### Mess with these couple of lines, and break all of the other defs! 
    apiendpoint = "/" + apiendpoint.lower()
    api1instance = urlparse(instanceurl)
    api1instance = api1instance.scheme + "://" + api1instance.netloc
    api1instance = api1instance + "/api"
    print(api1instance, apiendpoint, instanceurl)
    return instanceurl, apiendpoint, api1instance


####################################################################################################################################################################################
def main():
####################################################################################################################################################################################
# MAIN
    #Collect api server and endpoint. Also collect all of the instance json infomation we need into arrays with CollectUsrMenuItems
    CollectApiInfo()
    #print(instanceurl+apiendpoint)
 
    #Collects all users and info for instance and puts into array
    GetAllUsers()

    #Users
    if "users" in apiendpoint:
        User()
    

####################################################################################################################################################################################       
if __name__ == "__main__":
    main()     
####################################################################################################################################################################################






