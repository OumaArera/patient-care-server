from patient_project import settings

def build_absolute_url(file_path):
        """Build absolute URL for file path"""
        if not file_path:
            return None

        absolute_url = f"{settings.MEDIA_FULL_URL}/{file_path}"
        return absolute_url