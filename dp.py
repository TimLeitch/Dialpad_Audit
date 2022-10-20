from genericpath import exists
from queue import Empty
import re
from time import sleep
import requests
import configparser
import pandas as pd
import json


config = configparser.ConfigParser()
config.read('Dialpad_Audit\config.ini')

token = config['dialpad']['token']
path = './Recordings/Users/'

class Dialpad:   
   
   
    def list_users():
        """
        Gets a list of all users in the organization from Dialpad
        """
        url = "https://dialpad.com/api/v2/users"
        headers = {"accept": "application/json", "Authorization": "Bearer {}".format(token)}
        response = requests.get( url, headers=headers)
        users = response.json()['items']
        #print cursor value
        cursor = response.json()['cursor']
                  
        while cursor is not None:  
            response = requests.get(url+"?cursor="+response.json()['cursor'], headers=headers)
            users.extend(response.json()['items'])
            try:
                cursor = response.json()['cursor']
            except KeyError:
                cursor = None     
        return users  
      
    def get_recordings(user_id):
        """
        Get a list of recordings from Dialpad
        """
        url = "https://dialpad.com/api/v2/stats"

        payload = {
            "days_ago_end": 365,
            "days_ago_start": 1,
            "timezone": "America/Los_Angeles",
            "export_type": "records",
            "target_type": "user",
            "stat_type": "recordings",
            "target_id": "{}".format(user_id)
        }
        headers = {"accept": "application/json", "Authorization": "Bearer {}".format(token)}
        response = requests.post(url, json=payload, headers=headers)
        
        url = url+"/"+response.json()["request_id"]
        response = requests.get(url, headers=headers)
        
        while response.json()["status"] == "processing":
            sleep(0.5)
            response = requests.get(url, headers=headers)
            print(response.json()["status"])
        if response.json()["status"] == "failed":    
            return response.json()
                
        record = pd.read_csv(response.json()["download_url"])
        df = pd.DataFrame(record)
        if not df.empty:
            df.to_csv(path + str(user_id) +'_' + df['name'].iloc[0] + "_personal_recordings.csv")
            return df
        
        return None
        
    def get_office_recordings(office_id):
        """
        Get a list of office records from Dialpad
        """
        url = "https://dialpad.com/api/v2/stats"

        payload = {
            "days_ago_end": 365,
            "days_ago_start": 1,
            "timezone": "America/Los_Angeles",
            "export_type": "records",
            "stat_type": "recordings",
            "office_id": "{}".format(office_id)
        }
        headers = {"accept": "application/json", "Authorization": "Bearer {}".format(token)}
        response = requests.post(url, json=payload, headers=headers)

        url = url+"/"+response.json()["request_id"]
        response = requests.get(url, headers=headers)
        
        while response.json()["status"] == "processing":
            sleep(0.5)
            response = requests.get(url, headers=headers)
            print(response.json()["status"])
        if response.json()["status"] == "failed":         
            return None
                
        record = pd.read_csv(response.json()["download_url"])
        df = pd.DataFrame(record)
        if not df.empty:
            return df
        
        return None
    
    def list_offices():
        """
        Get a list of offices from Dialpad
        """
        url = "https://dialpad.com/api/v2/offices"
        headers = {"accept": "application/json", "Authorization": "Bearer {}".format(token)}
        response = requests.get(url, headers=headers)
        return response.json()