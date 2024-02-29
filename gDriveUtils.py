import os
import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# Hardcode credentials and token path
dump_path =  "C:/Users/Kris/Documents/houdini20.0/scripts/python/r_way_assignment_03/hou_to_gDrive"
creds_path = dump_path + "/credentials.json"
token_path = dump_path + "/token.json"

class gDriveUtils:
    def __init__(self):
        self.creds = None

    def getAuth(self):
        SCOPES = ['https://www.googleapis.com/auth/drive']

        if os.path.exists(token_path):
            self.creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    creds_path, SCOPES)
                self.creds = flow.run_local_server(port=0)
                    
            with open(token_path, "w") as token:
                token.write(self.creds.to_json())
        
    def checkDest(self, backup_folder_name):
        try:
            self.service = build("drive", "v3", credentials = self.creds)
            
            response = self.service.files().list(
                q=f"name='{backup_folder_name}' and mimeType='application/vnd.google-apps.folder'",
                spaces='drive'
            ).execute()      
            
            if not response["files"]:
                dir_metadata = {
                    "name": f"{backup_folder_name}",
                    "mimeType": "application/vnd.google-apps.folder"
                }

                file = self.service.files().create(body=dir_metadata, fields="id").execute()
            
                folder_id = file.get("id")
            else:
                folder_id = response["files"][0]["id"]

            return folder_id
 
        except HttpError as e:
            print("Error: " + str(e))
       
    def uploadFiles(self, folder_id):        
        for file in os.listdir(f"{dump_path}/geo"):
            file_metadata = {
                "name": file,
                "parents": [folder_id]
            }
        
            media = MediaFileUpload(f"{dump_path}/geo/{file}")
            upload_file = self.service.files().create(body=file_metadata,
                                                media_body=media,
                                                fields="id").execute()
            print("Backed up file: " + file)
                                                
    def run(self, backup_folder_name):
        self.getAuth()
        folder_id = self.checkDest(backup_folder_name)
        self.uploadFiles(folder_id)