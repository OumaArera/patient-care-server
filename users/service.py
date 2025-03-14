from core.utils.send_email import send_email
from core.utils.generate_random_password import generate_random_password
from users.repository import UserRepository
from core.utils.email_html import EmailHtmlContent
from users.serializers import UserSerializer
from core.dtos.user_dto import UserResponseDTO


class UserService:
    """Handles the business logic for user."""

    @staticmethod
    def create_user(data):
        """Creates a user in the database."""
        try:
            password = generate_random_password()
            data['is_staff'] = True
            data['password'] = password
            new_user = UserRepository.create_user(user_data=data)
            html_content = EmailHtmlContent.new_user_html(
                password=password,
                username=data.get('username'),
                recipient=data.get("firstName")
            )
            send_email(
                recipient_email=data.get('username'),
                recipient_name=data.get("firstName"),
                subject="User Creation!",
                html_content=html_content
            )
            return new_user
        except Exception as ex:
            raise ex
        
    @staticmethod
    def get_user_by_username(username):
        try:
            user = UserRepository.get_user_by_username(username=username)
            user = UserResponseDTO.transform_user(user)
            return user
        except Exception as ex:
            raise ex
        

    @staticmethod
    def block_user(username):
        try:
            user = UserRepository.block_user(username=username)
            serialized_user = UserSerializer(instance=user)
            return serialized_user.data
        except Exception as ex:
            raise ex
        

    @staticmethod
    def unblock_user(username):
        try:
            password = generate_random_password()
            user = UserRepository.unblock_user(username=username, password=password)
            html_content = EmailHtmlContent.new_user_html(
                password=password,
                username=user.username,
                recipient=user.firstName
            )
            send_email(
                recipient_email=user.username,
                recipient_name=user.firstName,
                subject="Account Activation!",
                html_content=html_content
            )
            serialized_user = UserSerializer(instance=user)
            return serialized_user.data
        except Exception as ex:
            raise ex
        
    @staticmethod
    def create_super_user(superuser_data):
        try:
            password = generate_random_password()
            superuser_data['password'] = password
            superuser = UserRepository.create_super_user(superuser_data)

            html_content = EmailHtmlContent.new_user_html(
                password=password,
                username=superuser_data.get('username'),
                recipient=superuser_data.get("firstName")
            )
            send_email(
                recipient_email=superuser_data.get('username'),
                recipient_name=superuser_data.get("firstName"),
                subject="Super User Creation!",
                html_content=html_content
            )
            return superuser
        except Exception as ex:
            raise ex

    @staticmethod
    def get_all_users(query_params):
        """Fetches and returns all users."""
        try:
            query_params.pop("pageSize", None)
            query_params.pop("pageNumber", None)
            users = UserRepository.get_all_users(
                query_params=query_params
            )
            return users
        except Exception as ex:
            raise ex

    @staticmethod
    def get_user_by_id(user_id):
        """Fetches the details of a user by ID."""
        try:
            user = UserRepository.get_user_by_user_id(user_id=user_id)
            user = UserResponseDTO.transform_user(user)
            return user
        except Exception as ex:
            raise ex
        

    @staticmethod
    def update_user(user_id, user_data):
        """Updates an existing user."""
        try:
            user = UserRepository.update_user(user_id=user_id, user_data=user_data)
            user = UserResponseDTO.transform_user(user)
            return user
        except Exception as ex:
            raise ex

    @staticmethod
    def delete_user(user_id):
        """Deletes a user by ID."""
        try:
            return UserRepository.delete_user(user_id=user_id)
        except Exception as ex:
            raise ex
