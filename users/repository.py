import logging
from core.db_exceptions import *
from django.db import IntegrityError, DatabaseError # type: ignore
from django.core.exceptions import ObjectDoesNotExist, ValidationError # type: ignore
from core.dtos.user_dto import UserResponseDTO
from core.utils.email_html import EmailHtmlContent
from core.utils.generate_random_password import generate_random_password
from core.utils.send_email import send_email
from users.models import User 

logger = logging.getLogger(__name__)

class UserRepository:
    """Handles the CRUD operations on the User model."""

    @staticmethod
    def create_user(user_data):
        """Creates a user in the database."""
        try:
            new_user = User.create_user(validated_data=user_data)
            new_user.full_clean()
            new_user.save()
            return new_user
        except ValidationError as ex:
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while creating a new user: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to create user.")
        except Exception as ex:
            logger.error(f"Unexpected error while creating a new user: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while creating user.")
        
    @staticmethod
    def create_super_user(superuser_data):
        try:
            superuser_data['is_staff'] = True
            superuser_data['is_superuser'] = True
            new_superuser = User.create_user(superuser_data)
            new_superuser.full_clean()
            new_superuser.save()
            return new_superuser
        except ValidationError as ex:
            raise IntegrityException(message=ex)
        except Exception as ex:
            logger.error(f"An error occurred while creating new user {ex}", exc_info=True)
            raise ex
        
    @staticmethod
    def update_user_password(username, password):
        try:
            user = User.objects.get_by_natural_key(username=username)
            if user.is_active:
                user.set_password(raw_password=password)
                user.save()
                return user
            raise ValidationError
        except ValidationError as ex:
            raise ValidationException(message="User account is inactive. Contact System administrator.")
        except User.DoesNotExist:
            raise NotFoundException(entity_name=f"User of username: {username}")
        except DatabaseError as ex:
            logger.error(f"Database error while fetching user by username: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to fetch user by username.")
        except Exception as ex:
            logger.error(f"Unexpected error while fetching user by username: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while fetching user by username.")
        
    @staticmethod
    def get_user_by_username(username):
        """Fetches user by username"""
        try:
            user = User.objects.get(username=username)
            return user
        except ObjectDoesNotExist:
            raise NotFoundException(entity_name='User with that username')
        except Exception as ex:
            logger.error(f"An error occurred while fetching user {ex}", exc_info=False)
            raise ex
        
    @staticmethod
    def block_user(username):
        """Fetches user by username and change status"""
        try:
            user = User.objects.get(username=username)
            user.is_active = False
            user.is_staff = False
            user.status = "blocked"
            user.save()
            return user
        except ObjectDoesNotExist:
            raise NotFoundException(entity_name='User with that username')
        except Exception as ex:
            logger.error(f"An error occurred while blocking user {ex}", exc_info=False)
            raise ex
        
    @staticmethod
    def unblock_user(username, password):
        """Fetches user by username and change their status"""
        try:
            user = User.objects.get(username=username)
            user.is_active = True
            user.is_staff = True
            user.status = "active"
            user.set_password(raw_password=password)
            user.save()
            return user
        except ObjectDoesNotExist:
            raise NotFoundException(entity_name='User with that username')
        except Exception as ex:
            logger.error(f"An error occurred while fetching user {ex}", exc_info=False)
            raise ex

    @staticmethod
    def get_all_users(query_params):
        """Fetches and returns all the users."""
        try:
            field_mapping = {
                "status": "status__icontains",
                "role": "role__icontains",
                "phoneNumber": "phoneNumber",
                "email": "email__icontains"
            }

            # Adjust filters to match the database field names
            adjusted_filters = {
                field_mapping.get(key, key): value
                for key, value in query_params.items()
                if value
            }

            # Query the database using filters
            users = User.objects.select_related(
                "branch"
            ).filter(
                **adjusted_filters
            ).values(
                "id",
                "avatar",
                "firstName",
                "middleNames",
                "lastName",
                "email",
                "phoneNumber",
                "sex",
                "role",
                "status",
                "branch__branchName",
                "branch__branchId",
                "branch__facility__facilityName",
                "dateOfBirth",
                "maritalStatus",
                "position",
                "credential",
                "credentialStatus",
                "dateEmployed",
                "supervisor",
                "provider",
                "employmentStatus"
            ).order_by('createdAt')

            return [UserResponseDTO.transform_user(user) for user in users]
        except DatabaseError as ex:
            logger.error(f"Database error while fetching users: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to fetch users.")
        except Exception as ex:
            logger.error(f"Unexpected error while fetching users: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while fetching users.")

    @staticmethod
    def get_user_by_user_id(user_id):
        """Fetches details of a user by ID."""
        try:
            user = User.objects.get(pk=user_id)
            return user
        except User.DoesNotExist:
            raise NotFoundException(entity_name=f"User of ID: {user_id}")
        except DatabaseError as ex:
            logger.error(f"Database error while fetching user by ID: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to fetch user by ID.")
        except Exception as ex:
            logger.error(f"Unexpected error while fetching user by ID: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while fetching user by ID.")

    @staticmethod
    def check_if_superuser_exists():
        try:
            superuser = User.objects.filter(role=True, is_superuser=True, status='active')
            if superuser:
                return True
            return False
        except Exception as ex:
            raise ex

    @staticmethod
    def update_user(user_id, user_data):
        """Updates the details of an existing user."""
        try:
            user = UserRepository.get_user_by_user_id(user_id=user_id)

            for field, value in user_data.items():
                if field == "password":
                    if value:
                        user.set_password(value)
                elif field == "employmentStatus":
                    if value in ["resigned", "dismissed"]:
                        user.is_active = False
                        user.is_staff = False
                        user.status = "blocked"
                        user.employmentStatus = value
                    elif value == "active":
                        user.is_active = True
                        user.is_staff = True
                        user.status = "active"

                        # Generate new password
                        password = generate_random_password()
                        user.set_password(password)

                        # Send email notification
                        html_content = EmailHtmlContent.new_user_html(
                            password=password,
                            username=user.username,
                            recipient=user.firstName
                        )
                        send_email(
                            recipient_email=user.username,
                            recipient_name=user.firstName,
                            subject="User Reactivation!",
                            html_content=html_content
                        )
                elif hasattr(user, field):
                    setattr(user, field, value)

            user.full_clean()
            user.save()
            return user

        except NotFoundException as ex:
            raise ex
        except ValidationError as ex:
            raise IntegrityException(message=str(ex))
        except DatabaseError as ex:
            logger.error(f"Database error while updating user: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to update user.")
        except Exception as ex:
            logger.error(f"Unexpected error while updating user: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while updating user.")


    @staticmethod
    def delete_user(user_id):
        """Deletes a user record by ID."""
        try:
            user = UserRepository.get_user_by_user_id(user_id=user_id)
            user.delete()
            return True
        except NotFoundException as ex:
            raise ex 
        except IntegrityError as ex:
            logger.error(f"Integrity error while deleting user: {ex}", exc_info=True)
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while deleting user: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to delete user.")
        except Exception as ex:
            logger.error(f"Unexpected error while deleting user: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while deleting user.")
