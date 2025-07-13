import os
from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/drive']

def authenticate(service_account_file):
    creds = service_account.Credentials.from_service_account_file(service_account_file, scopes=SCOPES)
    return creds

def upload_file(file_path, parent_folder_id, service_account_file):
    creds = authenticate(service_account_file)
    service = build('drive', 'v3', credentials=creds)
    file_metadata = {
        'name': os.path.basename(file_path),
        'parents': [parent_folder_id]
    }

    return service.files().create(body=file_metadata, media_body=file_path).execute()

def create_folder(folder_name, parent_folder_id, service_account_file):
    creds = authenticate(service_account_file)
    service = build('drive', 'v3', credentials=creds)
    file_metadata = {
        'name': folder_name,
        'mimeType': 'application/vnd.google-apps.folder',
        'parents': [parent_folder_id]
    }
    file = service.files().create(body=file_metadata, fields='id').execute()

    return file.get('id')
