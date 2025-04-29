# import os
# import json
# from rest_framework import serializers
# from core.utils.google_drive import GoogleDriveManager

# TYPE =os.getenv("TYPE")
# PROJECT_ID= os.getenv("PROJECT_ID")
# PRIVATE_KEY_ID=os.getenv("PRIVATE_KEY_ID")
# PRIVATE_KEY=os.getenv("PRIVATE_KEY")
# CLIENT_EMAIL=os.getenv("CLIENT_EMAIL")
# CLIENT_ID=os.getenv("CLIENT_ID")
# AUTH_URI=os.getenv("AUTH_URI")
# TOKEN_URI=os.getenv("TOKEN_URI")
# AUTH_PROVIDER_X509_CERT_URL=os.getenv("AUTH_PROVIDER_X509_CERT_URL")
# CLIENT_X509_CERT_URL=os.getenv("CLIENT_X509_CERT_URL")
# UNIVERSE_DOMAIN=os.getenv("UNIVERSE_DOMAIN")

# credentials = {
#     "type": TYPE,
#     "project_id": PROJECT_ID,
#     "private_key_id": PRIVATE_KEY_ID,
#     "private_key": PRIVATE_KEY,
#     "client_email": CLIENT_EMAIL,
#     "client_id": CLIENT_ID,
#     "auth_uri": AUTH_URI,
#     "token_uri": TOKEN_URI,
#     "auth_provider_x509_cert_url": AUTH_PROVIDER_X509_CERT_URL,
#     "client_x509_cert_url": CLIENT_X509_CERT_URL,
#     "universe_domain": UNIVERSE_DOMAIN
#   }

# drive_manager = GoogleDriveManager(credentials)

# class IncidentSerializer(serializers.Serializer):
#     """Serializer to validate the Incident data and upload a file to Google Drive."""

#     details = serializers.CharField()
#     filePath = serializers.FileField(write_only=True) 

#     def validate(self, data):
#         """
#         Custom validation: Uploads the file to Google Drive 
#         and replaces filePath with the Google Drive URL.
#         """
#         file = data.get("filePath")

#         if file:
#             temp_dir = "temp"
#             os.makedirs(temp_dir, exist_ok=True)  

#             file_path = os.path.join(temp_dir, file.name)

#             try:
#                 with open(file_path, "wb") as f:
#                     f.write(file.read())

#                 # Upload to Google Drive and get the public URL
#                 drive_url = drive_manager.upload_pdf(file_path, file.name)

#                 # Remove the local file after successful upload
#                 os.remove(file_path)

#                 # Replace filePath with the Google Drive URL
#                 data["filePath"] = drive_url

#             except Exception as e:
#                 raise serializers.ValidationError(f"File upload failed: {str(e)}")

#         return data

#     def process_incident(self, validated_data):
#         """
#         Returns the validated data with the Google Drive URL.
#         """
#         return {
#             "details": validated_data["details"],
#             "filePath": validated_data["filePath"],
#         }

# class IncidentUpdateSerializer(serializers.Serializer):
#     """Serializer for updating an Incident instance."""

#     details = serializers.CharField(required=False)
#     file = serializers.FileField(write_only=True, required=False)
#     status = serializers.ChoiceField(required=False, choices=["pending", "approved", "updated"])

#     def process_update(self, validated_data):
#         """
#         Handle updates to an incident without saving to DB.
#         If a new file is uploaded, it will be stored in Google Drive.
#         """
#         file_url = None
#         if "file" in validated_data:
#             file = validated_data.pop("file")
#             file_path = f"temp/{file.name}"

#             with open(file_path, "wb") as f:
#                 f.write(file.read())

#             file_url = drive_manager.upload_pdf(file_path, file.name)
#             os.remove(file_path)

#         return {
#             "details": validated_data.get("details"),
#             "filePath": file_url if file_url else "No file updated",
#             "status": validated_data.get("status"),
#         }
