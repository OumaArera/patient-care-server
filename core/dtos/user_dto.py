from core.utils.format_file_path import build_absolute_url
from core.utils.format_null_values import format_value


class UserResponseDTO:
    """User Response DTO"""
    
    @staticmethod
    def transform_user(data):
        """Transform Users data"""
        if isinstance(data, dict):
            return {
                "userId": data.get("id"),
                "avatar": build_absolute_url(data.get("avatar")),
                "fullName": format_value(
                    data.get("firstName"),
                    data.get("lastName")
                ),
                "email": data.get('email'),
                "phoneNumber": str(data.get("phoneNumber")),
                "sex": data.get("sex"),
                "role": data.get("role"),
                "status": data.get("status"),
                "branchName": data.get("branch__branchName"),
                "branchId": data.get("branch__branchId"),
                "facilityName": data.get("branch__facility__facilityName"),
            }
        else:
            return {
                "userId": data.id,
                "avatar": build_absolute_url(data.avatar),
                "fullName": format_value(
                    data.firstName,
                    data.lastName
                ),
                "email": data.email,
                "phoneNumber": str(data.phoneNumber),
                "sex": data.sex,
                "role": data.role,
                "status": data.status,
                "branchName": data.branch.branchName if data.branch else None,
                "branchId": data.branch.branchId if data.branch else None,
                "facilityName": data.branch.facility.facilityName\
                    if data.branch and data.branch.facility else None,
            }

    
