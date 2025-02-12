from core.utils.format_null_values import format_value

class AppointmentResponseDTO:
    """
    Data Transfer Object for Appointment Model
    """
    @staticmethod
    def transform_appointment(appointment):
        """
        Transforms an Appointment model instance into a dictionary.
        """
        if isinstance(appointment, dict):
            return {
                "appointmentId": appointment.get('appointmentId'),
                "patientId": appointment.get('patient__patientId'),
                "patientName": format_value(
                    appointment.get('patient__firstName'),
                    appointment.get('patient__lastName')
                ),
                "weeeklyAppointments": appointment.get('weeeklyAppointments'),
                "fortnightAppoints": appointment.get('fortnightAppoints'),
                "monthlyAppoints": appointment.get("monthlyAppoints"),
                "createdAt": appointment.get('createdAt')
            }
        else:
            return {
                "appointmentId": appointment.appointmentId,
                "patientId": appointment.patient.patientId,
                "patientName": format_value(
                    appointment.patient.firstName if appointment.patient else None,
                    appointment.patient.lastName if appointment.patient else None
                ),
                "weeeklyAppointments": appointment.weeeklyAppointments,
                "fortnightAppoints": appointment.fortnightAppoints,
                "monthlyAppoints": appointment.monthlyAppoints,
                "createdAt": appointment.createdAt
            }

    @staticmethod
    def transform_appointment_list(appointment_list):
        """
        Transforms a list of Appointment model instances into a list of dictionaries.
        """
        return [AppointmentResponseDTO.transform_appointment(data) for data in appointment_list]
