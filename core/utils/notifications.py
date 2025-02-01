import requests
from patient_project import settings


class Notifications:
	"""Handles email and sms notifications"""
	@staticmethod
	def send_sms(phone_number, message):
		"""
		Send SMS using the configured SMS provider.
		"""
		payload = {
			"to": phone_number,
			"message": message,
			"sender_id": settings.SMS_SENDER_ID,
			"api_key": settings.SMS_API_KEY
		}
		
		try:
			response = requests.post(settings.SMS_API_URL, json=payload)
			if response.status_code != 200:
				raise Exception("Failed to send SMS")
			print("SMS sent")
		except Exception as ex:
			print(f"SMS sending error: {ex}")
			
	@staticmethod
	def send_email(recipient, subject, html_content):
		"""Sends Email using the configured Email provider"""
		# Email payload
		email_payload = {
			"sender": {"email": settings.EMAIL_SENDER_ID, "name": "Istiwai Solutions"},
			"to": [{"email": recipient.email, "name": recipient.first_name}],
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