from custom_admin.repositories.branch_repo import BranchRepository
from core.dtos.branch_dto import BranchResponseDTO


class BranchService:
    """Handles the business logic for branches."""

    @staticmethod
    def create_branch(data):
        """Creates a branch in the database."""
        try:
            new_branch = BranchRepository.create_branch(branch_data=data)
            return BranchResponseDTO.transform_branch(branch=new_branch)
        except Exception as ex:
            raise ex

    @staticmethod
    def get_branch_by_id(branch_id):
        """Fetches details of a branch by ID."""
        try:
            branch = BranchRepository.get_branch_by_id(branch_id=branch_id)
            return BranchResponseDTO.transform_branch(branch=branch)
        except Exception as ex:
            raise ex

    @staticmethod
    def get_all_branches(query_params):
        """Fetches and returns all branches."""
        try:
            query_params.pop("pageSize", None)
            query_params.pop("pageNumber", None)
            branches = BranchRepository.get_all_branches(
                query_params=query_params
            )
            return branches
        except Exception as ex:
            raise ex

    @staticmethod
    def update_branch(branch_id, branch_data):
        """Updates an existing branch."""
        try:
            updated_branch = BranchRepository.update_branch(
                branch_id=branch_id, 
                branch_data=branch_data
            )
            return BranchResponseDTO.transform_branch(branch=updated_branch)
        except Exception as ex:
            raise ex

    @staticmethod
    def delete_branch(branch_id):
        """Deletes a branch by ID."""
        try:
            return BranchRepository.delete_branch(branch_id=branch_id)
        except Exception as ex:
            raise ex
