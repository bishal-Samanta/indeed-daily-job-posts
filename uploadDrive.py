from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()


def uploadToDrive(fileName):

    # Enter the path of the file you want to upload
    file_path = './sheet/Indeed Daily Job Posts.xlsx'




    # Enter the name that you want to give to the file on Google Drive
    file_name = fileName
    

    # Enter the ID of the folder where you want to upload the file (optional)
    folder_id = os.getenv('DRIVE_FOLDER_ID')

    # Set up the credentials
    creds = service_account.Credentials.from_service_account_file('credentials.json')

    # Set up the Drive API
    drive_service = build('drive', 'v3', credentials=creds)

    # Upload the file
    file_metadata = {'name': 'Indeed Daily Job Posts', 'parents': [folder_id]}
    media = MediaFileUpload(file_path, resumable=True)
    file = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
    
    print(f'Processed sheet uploaded to Drive with , File ID: {file.get("id")}')
    
