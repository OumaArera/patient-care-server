from custom_admin.repositories.appointments_repo import AppointmentRepository
from core.dtos.appointment_dto import AppointmentResponseDTO


class AppointmentService:
    """Handles the business logic for appointments."""

    @staticmethod
    def create_appointment(data):
        """Creates an appointment entry in the database."""
        try:
            new_appointment = AppointmentRepository.create_appointment(appointment_data=data)
            return AppointmentResponseDTO.transform_appointment(appointment=new_appointment)
        except Exception as ex:
            raise ex

    @staticmethod
    def get_appointment_by_id(appointment_id):
        """Fetches details of an appointment entry by ID."""
        try:
            appointment = AppointmentRepository.get_appointment_by_id(appointment_id=appointment_id)
            return AppointmentResponseDTO.transform_appointment(appointment=appointment)
        except Exception as ex:
            raise ex

    @staticmethod
    def get_all_appointments(query_params):
        """Fetches and returns all appointment data with optional filters."""
        try:
            query_params.pop("pageSize", None)
            query_params.pop("pageNumber", None)
            appointment_list = AppointmentRepository.get_all_appointments(query_params=query_params)
            return appointment_list
        except Exception as ex:
            raise ex

    @staticmethod
    def update_appointment(appointment_id, appointment_data):
        """Updates an existing appointment entry."""
        try:
            updated_appointment = AppointmentRepository.update_appointment(
                appointment_id=appointment_id, 
                appointment_data=appointment_data
            )
            return AppointmentResponseDTO.transform_appointment(appointment=updated_appointment)
        except Exception as ex:
            raise ex

    @staticmethod
    def delete_appointment(appointment_id):
        """Deletes an appointment entry by ID."""
        try:
            return AppointmentRepository.delete_appointment(appointment_id=appointment_id)
        except Exception as ex:
            raise ex