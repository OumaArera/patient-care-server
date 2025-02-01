class DataBaseException(Exception):
	"""
	Base class for database-related exceptions.
	"""
	
	def __init__(self, message=None, status_code=None):
		self.message = message or "Database error has occurred"
		self.status_code = status_code or 500
		super().__init__(self.message)


class NotFoundException(DataBaseException):
	"""
	Raised when a requested resource is not found in the database.
	"""
	
	def __init__(self, entity_name=None):
		message = f"{entity_name} does not exist" if entity_name else "Resource not found"
		status_code = 404
		super().__init__(message=message, status_code=status_code)


class IntegrityException(DataBaseException):
	"""
	Raised when database integrity is violated.
	"""
	
	def __init__(self, message=None):
		message = message or "Integrity constraint violation occurred"
		status_code = 400
		super().__init__(message=message, status_code=status_code)


class ValidationException(DataBaseException):
	"""
	Raised when invalid data is passed to the database.
	"""
	
	def __init__(self, message=None):
		message = message or "Invalid data provided"
		status_code = 422
		super().__init__(message=message, status_code=status_code)


class ConnectionException(DataBaseException):
	"""
	Raised when a database connection error occurs.
	"""
	
	def __init__(self, message=None):
		message = message or "Unable to connect to the database"
		status_code = 503
		super().__init__(message=message, status_code=status_code)


class TransactionException(DataBaseException):
	"""
	Raised when an error occurs during a database transaction.
	"""
	
	def __init__(self, message=None):
		message = message or "Database transaction error occurred"
		status_code = 500
		super().__init__(message=message, status_code=status_code)


class QueryException(DataBaseException):
	"""
	Raised when a database query fails.
	"""
	
	def __init__(self, message=None):
		message = message or "Error executing database query"
		status_code = 400
		super().__init__(message=message, status_code=status_code)