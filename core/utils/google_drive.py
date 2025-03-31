import googleapiclient.discovery  # type: ignore
import googleapiclient.http  # type: ignore
from google.oauth2.service_account import Credentials

class GoogleDriveManager:
    """
    A class to handle Google Drive file uploads and permissions.
    """

    def __init__(self, credentials: dict, scopes=None):
        """
        Initializes the Google Drive API client.
        :param credentials: Dictionary containing the service account credentials.
        :param scopes: List of API scopes (default: ["https://www.googleapis.com/auth/drive.file"])
        """
        if scopes is None:
            scopes = ["https://www.googleapis.com/auth/drive.file"]
        
        self.credentials = credentials
        self.scopes = scopes
        self.service = self.authenticate_google_drive()

    def authenticate_google_drive(self):
        """
        Authenticates and returns a Google Drive API service instance.
        """
        # creds = Credentials.from_service_account_file(self.credentials_path, scopes=self.scopes)
        creds = Credentials.from_service_account_info(self.credentials, scopes=self.scopes)

        service = googleapiclient.discovery.build("drive", "v3", credentials=creds)
        return service

    def make_file_public(self, file_id: str):
        """
        Sets a file's permissions to public.
        :param file_id: The ID of the file to make public.
        """
        permission = {
            "role": "reader",
            "type": "anyone"
        }
        self.service.permissions().create(fileId=file_id, body=permission).execute()

    def upload_pdf(self, file_path: str, file_name: str, folder_id: str = None) -> str:
        """
        Uploads a PDF file to Google Drive and makes it publicly accessible.
        :param file_path: Path to the PDF file to upload.
        :param file_name: Name of the file on Google Drive.
        :param folder_id: (Optional) Google Drive folder ID where the file should be uploaded.
        :return: Publicly accessible Google Drive download link.
        """
        file_metadata = {
            "name": file_name,
            "mimeType": "application/pdf",
        }

        if folder_id:
            file_metadata["parents"] = [folder_id]

        media = googleapiclient.http.MediaFileUpload(file_path, mimetype="application/pdf")

        uploaded_file = self.service.files().create(
            body=file_metadata,
            media_body=media,
            fields="id"
        ).execute()

        file_id = uploaded_file.get("id")

        # Make the file public
        self.make_file_public(file_id)

        # Generate a public download link
        file_url = f"https://drive.google.com/uc?export=download&id={file_id}"
        return file_url
