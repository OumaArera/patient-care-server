from django.http import JsonResponse # type: ignore

class EndpointNotFoundMiddleware:
	@staticmethod
	def APINotFoundException(request, exception):
		return JsonResponse(
			{
				'statusCode': '99',
				'statusMessage': 'The requested endpoint was not found on this server.',
				'successful': False
			}, 
			status=404)