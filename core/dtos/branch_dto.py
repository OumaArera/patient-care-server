class BranchResponseDTO:
    """
    Data Transfer Object for Branch Model
    """
    
    @staticmethod
    def transform_branch(branch):
        """
        Transforms a Branch model instance into a dictionary.
        """
        if isinstance(branch, dict):
            return {
                "branchId": branch.get('branchId'),
                "branchName": branch.get('branchName'),
                "branchAddress": branch.get('branchAddress'),
                "phoneNumber": branch.get('phoneNumber'),
                "email": branch.get('email'),
                "fax": branch.get("fax"),
                "facilityId": branch.get('facility_id'),
                "facilityName": branch.get("facility__facilityName")
            }
        else:
            return {
                "branchId": branch.branchId,
                "branchName": branch.branchName,
                "branchAddress": branch.branchAddress,
                "phoneNumber": branch.phoneNumber,
                "email": branch.email,
                "fax": branch.fax,
                "facility": branch.facility.facilityId,
                "facilityName": branch.facility.facilityName
            }
    
    @staticmethod
    def transform_branch_list(branches):
        """
        Transforms a list of Branch model instances into a list of dictionaries.
        """
        return [BranchResponseDTO.transform_branch(branch) for branch in branches]