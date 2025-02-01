class EmailHtmlContent:
	"""Generates Email Html Contents"""
	
	@staticmethod
	def new_user_html(password, username, recipient):
		html_content = \
		f"""
		<div>
			<h3>Dear {recipient}, you have been created on the XYZ Care Givers.</h3>
			<p>Your username is <strong>{username}</strong>.</p>
			<p>Your password is <strong>{password}</strong>.</p>
			<p>Use this link to login: http://localhost:3000/</p>
			<br />
			<p>Best Regards,</p>
			<footer>XYZ Team</footer>
		</div>
		"""
		return html_content
	
	@staticmethod
	def reset_password_html(password, username, recipient):
		html_content = \
		f"""
		<div>
			<h3>Dear {recipient}, your password has been reset.</h3>
			<p>Your username is <strong>{username}</strong>.</p>
			<p>Your new password is <strong>{password}</strong>.</p>
			<p>Use this link to login: http://localhost:3000/</p>
			<br />
			<p>Best Regards,</p>
			<footer>XYZ Team</footer>
		</div>
		"""
		return html_content
	
