from patient_project import settings
import requests # type: ignore


def send_email(recipient_email, recipient_name, subject, html_content):
		"""Sends Email using the configured Email provider"""
		# Email payload
		email_payload = {
			"sender": {"email": settings.EMAIL_SENDER_ID, "name": "1st Edmonds & Serenity Adult Family Homes"},
			"to": [{"email": recipient_email, "name": recipient_name}],
			"subject": subject,
			"htmlContent": html_content
		}
		
		# API headers
		headers = {
			"accept": "application/json",
			"api-key": settings.EMAIL_API_KEY,
			"content-type": "application/json"
		}
		
		try:
			# Send request
			response = requests.post(settings.EMAIL_API_URL, json=email_payload, headers=headers)
			# Check the response
			if response.status_code != 201:
				raise Exception("Failed to send email")
			print("Email sent")
		except Exception as ex:
			print(f"Failed to send email: {ex}")