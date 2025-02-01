
def format_validation_errors(error_obj):
	errors_arr = []
	for field, errors in error_obj.items():

		for error in errors:
			errors_arr.append(f"{field} : {str(error)}")
	return errors_arr