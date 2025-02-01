from django.http import Http404 # type: ignore
from rest_framework.views import exception_handler # type: ignore
from rest_framework.exceptions import AuthenticationFailed # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework import status # type: ignore

from core.utils.responses import APIResponse

def custom_exception_handler(exc, context):
  # 1. Call the default handler to get the standard error response.
  response = exception_handler(exc, context)
  # 2. Check if the exception is an instance of Authentication failed
  if isinstance(exc, AuthenticationFailed):
    return Response(
      data=APIResponse.error('99', 'Authentication failed', exc),
      status=response.status_code if response else status.HTTP_401_UNAUTHORIZED,
    )
  
  if isinstance(exc, Http404):
    return Response(
      data={"error": "The requested endpoint does not exist."},
      status=status.HTTP_404_NOT_FOUND
    )
  
  # 3. Return other exception responses unchanged
  return response