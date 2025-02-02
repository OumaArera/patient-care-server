class FacilityResponseDTO:
    """
    Data Transfer Object for Facility Model
    """
    
    @staticmethod
    def transform_facility(facility):
        """
        Transforms a Facility model instance into a dictionary.
        """
        if isinstance(facility, dict):
            return {
                "facilityId": facility.get('facilityId'),
                "facilityName": facility.get('facilityName'),
                "facilityAddress": facility.get('facilityAddress'),
            }
        else:
            return {
                "facilityId": facility.facilityId,
                "facilityName": facility.facilityName,
                "facilityAddress": facility.facilityAddress,
            }
    
    @staticmethod
    def transform_facility_list(facilities):
        """
        Transforms a list of Facility model instances into a list of dictionaries.
        """
        return [FacilityResponseDTO.transform_facility(facility) for facility in facilities]
