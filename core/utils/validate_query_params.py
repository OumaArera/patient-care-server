from rest_framework.exceptions import ValidationError # type: ignore

def validate_query_params(query_params, valid_query_params):
	valid_params = {}
	invalid_params = []
	for key, value in query_params.items():
		if key not in valid_query_params:
			invalid_params.append(key)
			
		else:
			valid_params[key]=value
			
			
	if invalid_params:
		raise ValidationError(f"Invalid query parameters: {', '.join(invalid_params)}")
	else:
		return valid_params


