import logging
from core.db_exceptions import *
from django.db import IntegrityError, DatabaseError  # type: ignore
from django.core.exceptions import ValidationError  # type: ignore
from core.dtos.appointment_dto import AppointmentResponseDTO
from custom_admin.models.appointment import Appointment
from custom_admin.models.patient import Patient

logger = logging.getLogger(__name__)

class AppointmentRepository:
    """Handles CRUD operations on the Appointment model."""

    @staticmethod
    def create_appointment(appointment_data):
        """Creates an appointment in the database."""
        try:
            new_appointment = Appointment.create_appointment(appointment_data)
            new_appointment.full_clean()
            new_appointment.save()
            return new_appointment
        except ValidationError as ex:
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while creating appointment: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to create appointment.")
        except Exception as ex:
            logger.error(f"Unexpected error while creating appointment: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while creating appointment.")

    @staticmethod
    def get_appointment_by_id(appointment_id):
        """Fetches appointment details by ID."""
        try:
            appointment = Appointment.objects.get(pk=appointment_id)
            return appointment
        except Appointment.DoesNotExist:
            raise NotFoundException(entity_name=f"Appointment with ID: {appointment_id}")
        except DatabaseError as ex:
            logger.error(f"Database error while fetching appointment by ID: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to fetch appointment by ID.")
        except Exception as ex:
            logger.error(f"Unexpected error while fetching appointment by ID: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while fetching appointment by ID.")

    @staticmethod
    def get_all_appointments(query_params):
        """Fetches and returns all appointments with optional filtering."""
        try:
            field_mapping = {
                "patient": "patient__patientId",
            }

            adjusted_filters = {
                field_mapping.get(key, key): value
                for key, value in query_params.items()
                if value
            }

            appointments = Appointment.objects.select_related(
                "patient"
            ).filter(
                **adjusted_filters
            ).values(
                "appointmentId", "weeklyAppointments", 
                "fortnightAppointments", "monthlyAppointments",
                "patient__firstName", "patient__lastName", 
                "patient__patientId", "createdAt", "attendedTo"
            ).order_by("createdAt") 
            
            return [AppointmentResponseDTO.transform_appointment(data) for data in appointments]
        except DatabaseError as ex:
            logger.error(f"Database error while fetching appointments: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to fetch appointments.")
        except Exception as ex:
            logger.error(f"Unexpected error while fetching appointments: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while fetching appointments.")

    @staticmethod
    def update_appointment(appointment_id, appointment_data):
        """Updates an existing appointment."""
        try:
            appointment = AppointmentRepository.get_appointment_by_id(appointment_id=appointment_id)
            for field, value in appointment_data.items():
                if hasattr(appointment, field):  
                    setattr(appointment, field, value)
            appointment.full_clean()
            appointment.save()
            return appointment
        except NotFoundException as ex:
            raise ex
        except ValidationError as ex:
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while updating appointment: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to update appointment.")
        except Exception as ex:
            logger.error(f"Unexpected error while updating appointment: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while updating appointment.")

    @staticmethod
    def delete_appointment(appointment_id):
        """Deletes an appointment record by ID."""
        try:
            appointment = AppointmentRepository.get_appointment_by_id(appointment_id=appointment_id)
            appointment.delete()
            return True
        except NotFoundException as ex:
            raise ex
        except IntegrityError as ex:
            logger.error(f"Integrity error while deleting appointment: {ex}", exc_info=True)
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while deleting appointment: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to delete appointment.")
        except Exception as ex:
            logger.error(f"Unexpected error while deleting appointment: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while deleting appointment.")
