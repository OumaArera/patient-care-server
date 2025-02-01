from core.utils.notifications import Notifications
from core.utils.email_html import EmailHtmlContent


def send_password(user, password):
	try:
		html_content = EmailHtmlContent.reset_password_html(password=password)
		Notifications.send_email(recipient=user, subject='Password Reset', html_content=html_content)
	except Exception:
		raise