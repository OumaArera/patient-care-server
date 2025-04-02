import logging
from django.db import IntegrityError, DatabaseError
from django.core.exceptions import ValidationError
from core.db_exceptions import *
from core.dtos.leave_dto import LeaveResponseDTO  
from core.utils.email_html import EmailHtmlContent
from core.utils.send_email import send_email
from custom_admin.models.leave import Leave

logger = logging.getLogger(__name__)

class LeaveRepository:
    """Handles CRUD operations on the Leave model."""

    @staticmethod
    def create_leave(leave_data):
        """Creates a new leave entry in the database."""
        try:
            new_leave = Leave.create_leave(validated_data=leave_data)
            new_leave.full_clean()
            new_leave.save()

            # Send notification emails
            recipients = [
                {"name": "Nixon Duah", "email": "nixon.duah@edmondserenity.com"},
                {"name": "David Obuya", "email": "david.obuya@edmondserenity.com"}
            ]
            staff = f"{new_leave.staff.firstName} {new_leave.staff.lastName}" if new_leave.staff else "Unknown Staff"
            for recipient in recipients:
                html_body = EmailHtmlContent.leave_request_html(
                    supervisor=recipient["name"],
                    staff_name=staff,
                    reason=new_leave.reasonForLeave
                )
                send_email(
                    recipient_email=recipient["email"],
                    recipient_name=recipient["name"],
                    subject="Leave Request",
                    html_content=html_body
                )

            return new_leave
        except ValidationError as ex:
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while creating a new leave: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to create leave.")
        except Exception as ex:
            logger.error(f"Unexpected error while creating a new leave: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while creating leave.")

    @staticmethod
    def get_leave_by_id(leave_id):
        """Fetches details of a leave by ID."""
        try:
            leave = Leave.objects.get(pk=leave_id)
            return leave
        except Leave.DoesNotExist:
            raise NotFoundException(entity_name=f"Leave with ID: {leave_id}")
        except DatabaseError as ex:
            logger.error(f"Database error while fetching leave by ID: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to fetch leave by ID.")
        except Exception as ex:
            logger.error(f"Unexpected error while fetching leave by ID: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while fetching leave by ID.")

    @staticmethod
    def get_all_leaves(query_params):
        """Fetches and returns all leaves with optional filtering."""
        try:
            field_mapping = {
                "staff": "staff_id",
                "startDate": "startDate",
                "endDate": "endDate",
                "status": "status__icontains"
            }

            adjusted_filters = {
                field_mapping.get(key, key): value
                for key, value in query_params.items()
                if value
            }

            leaves = Leave.objects.select_related(
                "staff"
            ).filter(
                **adjusted_filters
            ).values(
                "leaveId",
                "reasonForLeave",
                "startDate",
                "endDate",
                "createdAt",
                "modifiedAt",
                "status",
                "declineReason",
                "staff__id",
                "staff__firstName",
                "staff__lastName"
            ).order_by("startDate")

            # leaves = paginator.paginate_queryset(queryset=leaves, request=request)
            return [LeaveResponseDTO.transform_leave(leave) for leave in leaves]
        except DatabaseError as ex:
            logger.error(f"Database error while fetching leaves: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to fetch leaves.")
        except Exception as ex:
            logger.error(f"Unexpected error while fetching leaves: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while fetching leaves.")

    @staticmethod
    def update_leave(leave_id, leave_data):
        """Updates the details of an existing leave."""
        try:
            leave = LeaveRepository.get_leave_by_id(leave_id=leave_id)
            status_updated = False
            for field, value in leave_data.items():
                if hasattr(leave, field):
                    if field == "status" and getattr(leave, field) != value:
                        status_updated = True
                    setattr(leave, field, value)
            leave.full_clean()
            leave.save()

            if status_updated:
                staff_name = f"{leave.staff.firstName} {leave.staff.lastName}"
                html_body = EmailHtmlContent.leave_status_update_html(
                    staff_name,
                    leave.status,
                    leave.reasonForLeave
                )

                send_email(
                    recipient_email=leave.staff.email,
                    recipient_name=leave.staff.firstName,
                    subject=f"Leave status update for {leave.staff.firstName} {leave.staff.lastName}",
                    html_content=html_body
                )

            return leave
        except NotFoundException as ex:
            raise ex
        except ValidationError as ex:
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while updating leave: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to update leave.")
        except Exception as ex:
            logger.error(f"Unexpected error while updating leave: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while updating leave.")

    @staticmethod
    def delete_leave(leave_id):
        """Deletes a leave record by ID."""
        try:
            leave = LeaveRepository.get_leave_by_id(leave_id=leave_id)
            leave.delete()
            return True
        except NotFoundException as ex:
            raise ex
        except IntegrityError as ex:
            logger.error(f"Integrity error while deleting leave: {ex}", exc_info=True)
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while deleting leave: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to delete leave.")
        except Exception as ex:
            logger.error(f"Unexpected error while deleting leave: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while deleting leave.")
