from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload
from google.oauth2.service_account import Credentials
import io
import os

# Load Google Drive API credentials
SERVICE_ACCOUNT_FILE = "./acadassistdrive.json"
SCOPES = ["https://www.googleapis.com/auth/drive"]

credentials = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
drive_service = build("drive", "v3", credentials=credentials)

def create_folder(folder_name, parent_id=None):
    """Create a folder in Google Drive."""
    file_metadata = {
        "name": folder_name,
        "mimeType": "application/vnd.google-apps.folder",
    }
    if parent_id:
        file_metadata["parents"] = [parent_id]
    folder = drive_service.files().create(body=file_metadata, fields="id").execute()
    return folder.get("id")

def upload_file(file_path, file_name, folder_id):
    """Upload a file to Google Drive."""
    file_metadata = {"name": file_name, "parents": [folder_id]}
    media = MediaFileUpload(file_path)
    file = drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()
    return file.get("id")

def list_files(folder_id):
    """List files in a specific Google Drive folder."""
    try:
        query = f"'{folder_id}' in parents and trashed = false"
        results = drive_service.files().list(q=query, fields="files(id, name)").execute()
        return results.get("files", [])
    except Exception as e:
        print(f"Error listing files in folder {folder_id}: {e}")
        raise ValueError(f"Failed to list files. Ensure the folder ID '{folder_id}' is correct and accessible.")

def download_file(file_id, destination_path):
    """Download a file from Google Drive."""
    try:
        # Get file metadata to get the original file name
        file_metadata = drive_service.files().get(fileId=file_id, fields='name').execute()
        original_name = file_metadata.get('name', 'downloaded_file')
        
        # Create the full destination path with the original file name
        directory = os.path.dirname(destination_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        # Create a unique file name if the file already exists
        base_name, extension = os.path.splitext(original_name)
        counter = 1
        final_path = os.path.join(directory, original_name)
        
        while os.path.exists(final_path):
            final_path = os.path.join(directory, f"{base_name}_{counter}{extension}")
            counter += 1
        
        # Download the file
        request = drive_service.files().get_media(fileId=file_id)
        with open(final_path, "wb") as file:
            downloader = MediaIoBaseDownload(file, request)
            done = False
            while not done:
                status, done = downloader.next_chunk()
        
        return final_path
    except Exception as e:
        print(f"Error downloading file {file_id}: {e}")
        raise ValueError(f"Failed to download file. Error: {str(e)}")

def remove_file(file_id):
    """Remove a file from Google Drive."""
    try:
        drive_service.files().delete(fileId=file_id).execute()
        return True
    except Exception as e:
        print(f"Error removing file {file_id}: {e}")
        raise ValueError(f"Failed to remove file. Ensure the file ID '{file_id}' is correct and you have permission to delete it.")
