from contextlib import nullcontext
from importlib.machinery import OPTIMIZED_BYTECODE_SUFFIXES
from dp import Dialpad
import pandas as pd
import os

path = './Recordings/Users/'
if not os.path.exists(path):
    os.makedirs(path)

office = Dialpad.list_offices()   
for each in office['items']:
    officeID = each["id"]
    officeName = each["name"]
    print(officeName)
    officeRecordings = Dialpad.get_office_recordings(officeID)
    print(officeRecordings)
    if officeRecordings is not None:
        for each in officeRecordings["operator_id"].unique():
            df2 = officeRecordings[officeRecordings["operator_id"] == each]
            if df2["operator_name"].empty:
                df2.to_csv(path+str(each) + ".csv") 
            else:
                df2.to_csv(path+str(each) + "_" + df2["operator_name"].iloc[0] + ".csv")


users = Dialpad.list_users()
for each in users:
    userID = each["id"]
    print(each['first_name'] + " " + each['last_name'])
    userRecordings = Dialpad.get_recordings(userID)
    
