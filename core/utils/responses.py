class APIResponse:
	"""Structures a uniform API Response"""
	@staticmethod
	def success(code, message, data):
		"""Returns a success response"""
		res = {
			'statusCode':code,
			'statusMessage':message,
			'successful': True,
			'responseObject': data
		}
		return res

	@staticmethod
	def error(code, message, error):
		"""Returns an error response"""
		res = {
			'statusCode': code,
			'statusMessage': message,
			'successful': False,
			'responseObject': {
				'errors': getattr(error, 'detail', None) if getattr(error, 'detail', None) else str(error),
			}
		}
		return  res