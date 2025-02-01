from secrets import token_urlsafe

def generate_random_password():
	"""
	Generate a secure random password.
	"""
	return token_urlsafe(10)