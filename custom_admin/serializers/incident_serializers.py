import os
from rest_framework import serializers
from core.utils.google_drive import GoogleDriveManager

# Define the credentials file path at the root directory
CREDENTIALS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), ".", "credentials.json"))

# Initialize Google Drive Manager
drive_manager = GoogleDriveManager(CREDENTIALS_PATH)

class IncidentSerializer(serializers.Serializer):
    """Serializer to validate the Incident data and upload a file to Google Drive."""

    details = serializers.CharField()
    filePath = serializers.FileField(write_only=True)  # File upload field

    def validate(self, data):
        """
        Custom validation: Uploads the file to Google Drive 
        and replaces filePath with the Google Drive URL.
        """
        file = data.get("filePath")

        if file:
            temp_dir = "temp"
            os.makedirs(temp_dir, exist_ok=True)  

            file_path = os.path.join(temp_dir, file.name)

            try:
                with open(file_path, "wb") as f:
                    f.write(file.read())

                # Upload to Google Drive and get the public URL
                drive_url = drive_manager.upload_pdf(file_path, file.name)

                # Remove the local file after successful upload
                os.remove(file_path)

                # Replace filePath with the Google Drive URL
                data["filePath"] = drive_url

            except Exception as e:
                raise serializers.ValidationError(f"File upload failed: {str(e)}")

        return data

    def process_incident(self, validated_data):
        """
        Returns the validated data with the Google Drive URL.
        """
        return {
            "details": validated_data["details"],
            "filePath": validated_data["filePath"],
        }

class IncidentUpdateSerializer(serializers.Serializer):
    """Serializer for updating an Incident instance."""

    details = serializers.CharField(required=False)
    file = serializers.FileField(write_only=True, required=False)
    status = serializers.ChoiceField(required=False, choices=["pending", "approved", "updated"])

    def process_update(self, validated_data):
        """
        Handle updates to an incident without saving to DB.
        If a new file is uploaded, it will be stored in Google Drive.
        """
        file_url = None
        if "file" in validated_data:
            file = validated_data.pop("file")
            file_path = f"temp/{file.name}"

            with open(file_path, "wb") as f:
                f.write(file.read())

            file_url = drive_manager.upload_pdf(file_path, file.name)
            os.remove(file_path)

        return {
            "details": validated_data.get("details"),
            "filePath": file_url if file_url else "No file updated",
            "status": validated_data.get("status"),
        }
