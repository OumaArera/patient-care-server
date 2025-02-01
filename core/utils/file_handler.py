import os

from patient_project import settings


def handle_file(file, directory):
	# Save the file
	resources_dir = os.path.join(settings.MEDIA_ROOT, directory)
	os.makedirs(resources_dir, exist_ok=True)
	file_path = os.path.join(resources_dir, file.name)

	with open(file_path, 'wb') as destination:
		for chunk in file.chunks():
			destination.write(chunk)

	return os.path.relpath(file_path, settings.MEDIA_ROOT)