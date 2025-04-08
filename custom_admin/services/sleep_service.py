from custom_admin.repositories.sleep_repo import SleepRepository

class SleepService:
    """Handles the business logic for sleep entries."""

    @staticmethod
    def create_sleep(data):
        """Creates a new sleep entry in the database."""
        try:
            new_sleep = SleepRepository.create_sleep(sleep_data=data)
            return SleepService.transform_sleep(new_sleep)
        except Exception as ex:
            raise ex

    @staticmethod
    def get_sleep_by_id(sleep_id):
        """Fetches details of a sleep entry by ID."""
        try:
            sleep = SleepRepository.get_sleep_by_id(sleep_id=sleep_id)
            return SleepService.transform_sleep(sleep)
        except Exception as ex:
            raise ex

    @staticmethod
    def get_all_sleeps(query_params):
        """Fetches and returns all sleep entries with optional filtering."""
        try:
            # Remove pagination parameters if present
            query_params.pop("pageSize", None)
            query_params.pop("pageNumber", None)

            sleep_entries = SleepRepository.get_all_sleeps(query_params=query_params)
            return [SleepService.transform_sleep_dict(sleep) for sleep in sleep_entries]
        except Exception as ex:
            raise ex

    @staticmethod
    def update_sleep(sleep_id, sleep_data):
        """Updates an existing sleep entry."""
        try:
            updated_sleep = SleepRepository.update_sleep(
                sleep_id=sleep_id,
                sleep_data=sleep_data
            )
            return SleepService.transform_sleep(updated_sleep)
        except Exception as ex:
            raise ex

    @staticmethod
    def delete_sleep(sleep_id):
        """Deletes a sleep entry by ID."""
        try:
            return SleepRepository.delete_sleep(sleep_id=sleep_id)
        except Exception as ex:
            raise ex

    @staticmethod
    def transform_sleep(sleep):
        """Transforms a Sleep model instance to a serializable dictionary."""
        return {
            "incidentId": sleep.sleepId,
            "markAs": sleep.markAs,
            "markedFor": sleep.markedFor,
            "dateTaken": sleep.dateTaken,
            "createdAt": sleep.createdAt,
            "modifiedAt": sleep.modifiedAt,
            "reasonFilledLate": sleep.reasonFilledLate,
            "resident": {
                "patientId": sleep.resident.patientId if sleep.resident else None,
                "firstName": sleep.resident.firstName if sleep.resident else None,
                "lastName": sleep.resident.lastName if sleep.resident else None
            } if sleep.resident else None
        }

    @staticmethod
    def transform_sleep_dict(sleep_dict):
        """Transforms a dictionary sleep entry (from `.values(...)`) to a cleaner response format."""
        return {
            "sleepId": sleep_dict["sleepId"],
            "markAs": sleep_dict["markAs"],
            "markedFor": sleep_dict["markedFor"],
            "dateTaken": sleep_dict["dateTaken"],
            "createdAt": sleep_dict["createdAt"],
            "modifiedAt": sleep_dict["modifiedAt"],
            "reasonFilledLate": sleep_dict['reasonFilledLate'],
            "resident": {
                "patientId": sleep_dict["resident__patientId"],
                "firstName": sleep_dict["resident__firstName"],
                "lastName": sleep_dict["resident__lastName"]
            } if sleep_dict["resident__patientId"] else None
        }
