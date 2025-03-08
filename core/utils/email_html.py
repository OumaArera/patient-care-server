class EmailHtmlContent:
	"""Generates Email Html Contents"""
	
	@staticmethod
	def new_user_html(password, username, recipient):
		html_content = \
		f"""
		<div>
			<h4>Dear <strong>{recipient}</strong>,</h4>
			<p>You have been created on the 1st Edmonds & Serenity Adult Family Homes.</p>
			<p>Your username is <strong>{username}</strong></p>
			<p>Your password is <strong>{password}</strong></p>
			<p>Use this link to login: https://edmondserenity.com/</p>
			<br />
			<p>Best Regards,</p>
			<footer>1st Edmonds & Serenity Adult Family Homes</footer>
		</div>
		"""
		return html_content
	
	@staticmethod
	def reset_password_html(password, username, recipient):
		html_content = \
		f"""
		<div>
			<h4>Dear <strong>{recipient}</strong>,</h4>
			<p>Your password for 1st Edmonds & Serenity Adult Family Homes</p>
			<p>has been reset successfully</p>
			<p>Your username is <strong>{username}</strong></p>
			<p>Your new password is <strong>{password}</strong></p>
			<p>Use this link to login: https://edmondserenity.com/</p>
			<br />
			<p>Best Regards,</p>
			<footer>1st Edmonds & Serenity Adult Family Homes</footer>
		</div>
		"""
		return html_content


	@staticmethod
	def chart_update_html(recipient, resident, status):
		html_content = \
		f"""
		<div>
			<h4>Dear <strong>{recipient}</strong>,</h4>
			<p>An update has been made on the chart for {resident}</p>
			<p>The status has been changed to {status}</p>
			<p>Please login to your account and for any further action</p>
			<p>Use this link to login: https://edmondserenity.com/</p>
			<br />
			<p>Best Regards,</p>
			<footer>1st Edmonds & Serenity Adult Family Homes</footer>
		</div>
		"""
		return html_content
	
