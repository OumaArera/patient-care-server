from rest_framework.exceptions import * # type: ignore
from django.utils.translation import gettext_lazy as _ # type: ignore
from rest_framework import status # type: ignore

class CustomNotAuthenticated(APIException):
  """
  Custom exception to return 401 Unauthorized.
  """
  status_code = status.HTTP_401_UNAUTHORIZED
  default_detail = _('Authentication credentials were not provided.')
  default_code = 'not_authenticated'
  
  def __init__(self, detail=None, code=None, status_code=None):
    # Update the status code if provided
    if status_code is not None:
      self.status_code = status_code
    
    # Call the parent class to handle the rest
    super().__init__(detail=detail, code=code)