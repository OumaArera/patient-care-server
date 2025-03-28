class EmailHtmlContent:
	"""Generates Email Html Contents"""
	
	@staticmethod
	def assessment_notification_html(resident, assessment_date, recipient, branch, socialWorker):
		""""""
		html_content = \
		f"""
			<div>
			<h4>Dear {recipient},</h4>
			<p>{resident}, resident at {branch} has an upcoming assessment as below:</p>
			<p>{assessment_date}</p>
			<p>Social Worker /Case Manager {socialWorker}</p>
			<br />
			<p>Best Regards,</p>
			<footer>1st Edmonds & Serenity Adult Family Homes</footer>
		</div>
		"""
		return html_content

	@staticmethod
	def incident_notification_html(details, file_path, staff, recipient):
		""""""
		html_content = \
		f"""
			<div>
			<h4>Dear {recipient},</h4>
			<p>An incident has been reported as below by <strong>{staff}</strong> for your action:</p>
			<br />
			<p>{details}</p>
			<p>{file_path}</p>
			<br />
			<p>Best Regards,</p>
			<footer>1st Edmonds & Serenity Adult Family Homes</footer>
		</div>
		"""
		return html_content

	@staticmethod
	def grocery_notification_html(recipient, branch, staff, details):
		"""Generate HTML content for grocery notification email."""
		table_rows = "".join(
			f"<tr><td>{item['item']}</td><td>{item['quantity']}</td></tr>"
			for item in details
		)

		html_content = f"""
			<div>
				<h4>Dear {recipient},</h4>
				<p>The following groceries have been requested by <strong>{staff}</strong>.</p>
				<br />
				<h3>{branch}</h3>
				<table border="1" cellpadding="5" cellspacing="0" style="border-collapse: collapse; width: 50%;">
					<thead>
						<tr>
							<th>Item</th>
							<th>Quantity</th>
						</tr>
					</thead>
					<tbody>
						{table_rows}
					</tbody>
				</table>
				<br />
				<p>Best Regards,</p>
				<footer>1st Edmonds & Serenity Adult Family Homes</footer>
			</div>
		"""
		return html_content
	

	@staticmethod
	def utility_notification_html(recipient, staff, item, details):
		""""""
		html_content = \
		f"""
			<div>
			<h4>Dear {recipient},</h4>
			<p>An incident has been reported as below by <strong>{staff}</strong> for your action:</p>
			<br />
			<p>{item}</p>
			<p>{details}</p>
			<br />
			<p>Best Regards,</p>
			<footer>1st Edmonds & Serenity Adult Family Homes</footer>
		</div>
		"""
		return html_content



	@staticmethod
	def leave_status_update_html(staff_name, status, reason):
		html_content = \
		f"""
			<div>
			<h4>Dear <strong>{staff_name}</strong>,</h4>
			<p>You leave request with the below details has been reviewed.</p>
			<br />
			<p>{reason}</p>
			<br />
			<p>The status is <strong>{status}</strong>.</p>
			<p>Please reach out to your supervisor for further instructions.</p>
			<br />
			<p>Best Regards,</p>
			<footer>1st Edmonds & Serenity Adult Family Homes</footer>
		</div>
		"""
		return html_content
	
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
	
	@staticmethod
	def generate_html(recipient, message):
		sentences = message.split(". ")
		formatted_message = "".join(f"<p>{sentence.strip()}.</p>" for sentence in sentences if sentence)

		html_content = f"""
		<div style="font-family: Arial, sans-serif; color: #333;">
			<h4>Dear <strong>{recipient}</strong>, Happy Birthday! 🎉</h4>
			{formatted_message}
			<br />
			<p>Best Regards,</p>
			<footer>1st Edmonds & Serenity Adult Family Homes</footer>
		</div>
		"""
		return html_content

	
