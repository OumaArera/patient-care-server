from rest_framework import status # type: ignore
from rest_framework.exceptions import UnsupportedMediaType  # type: ignore
from rest_framework.response import Response # type: ignore
from rest_framework.views import APIView # type: ignore
from core.db_exceptions import IntegrityException
from core.permissions import IsSuperUser
from core.utils.responses import APIResponse
from users.service import UserService

class BlockUserView(APIView):
    """
    Receives username and makes request to block the user
    """
    permission_classes = [IsSuperUser]
	
    def post(self, request):
        """
        Handles user blocking.
        """
        try:
            
            if request.content_type != 'application/json':
                raise UnsupportedMediaType(media_type=request.content_type)
                
            username = request.data.get('username')
            
            if not username:
                raise IntegrityException(message="Username must be provided")
            
            if username == request.user.username:
                raise IntegrityException(message="User cannot self block")
            
            bolcked_user = UserService.block_user(
                username=username
            )

            return Response(
                APIResponse.success(
                    code="00",
                    message="User blocked successfully",
                    data=bolcked_user
                ),
                status=status.HTTP_200_OK
            )
                
        except Exception as ex:
            return Response(
                data=APIResponse.error('99', "An error occurred while blocking user", error=ex),
                status=ex.status_code,
                content_type='application/json'
            )
        

class UnBlockUserView(APIView):
    """
    Receives username and makes request to unblock the user
    """
    permission_classes = [IsSuperUser]
	
    def post(self, request):
        """
        Handles user unblocking.
        """
        try:
            
            if request.content_type != 'application/json':
                raise UnsupportedMediaType(media_type=request.content_type)
                
            username = request.data.get('username')
            
            if not username:
                raise IntegrityException(message="Username must be provided")
            
            unblocked_user = UserService.unblock_user(
                username=username
            )

            return Response(
                APIResponse.success(
                    code="00",
                    message="User unblocked successfully",
                    data=unblocked_user
                ),
                status=status.HTTP_200_OK
            )
                
        except Exception as ex:
            return Response(
                data=APIResponse.error('99', "An error occurred while unblocking user", error=ex),
                status=ex.status_code,
                content_type='application/json'
            )