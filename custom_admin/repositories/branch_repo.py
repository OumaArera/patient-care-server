import logging
from core.db_exceptions import *
from django.db import IntegrityError, DatabaseError  # type: ignore
from django.core.exceptions import ValidationError  # type: ignore
from core.dtos.branch_dto import BranchResponseDTO
from core.paginator import paginator
from custom_admin.models.branch import Branch

logger = logging.getLogger(__name__)


class BranchRepository:
    """Handles the CRUD operations on the Branch model."""

    @staticmethod
    def create_branch(branch_data):
        """Creates a branch in the database."""
        try:
            new_branch = Branch.create_branch(validated_data=branch_data)
            new_branch.full_clean()
            new_branch.save()
            return new_branch
        except ValidationError as ex:
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while creating a new branch: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to create branch.")
        except Exception as ex:
            logger.error(f"Unexpected error while creating a new branch: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while creating branch.")

    @staticmethod
    def get_branch_by_id(branch_id):
        """Fetches details of a branch by ID."""
        try:
            branch = Branch.objects.get(pk=branch_id)
            return branch
        except Branch.DoesNotExist:
            raise NotFoundException(entity_name=f"Branch with ID: {branch_id}")
        except DatabaseError as ex:
            logger.error(f"Database error while fetching branch by ID: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to fetch branch by ID.")
        except Exception as ex:
            logger.error(f"Unexpected error while fetching branch by ID: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while fetching branch by ID.")

    @staticmethod
    def get_all_branches(query_params):
        """Fetches and returns all the branches with optional filtering."""
        try:
            field_mapping = {
                "branchName": "branchName__icontains",
                "branchAddress": "branchAddress__icontains",
                "facility": "facility__facilityId",
            }

            adjusted_filters = {
                field_mapping.get(key, key): value
                for key, value in query_params.items()
                if value
            }

            branches = Branch.objects.select_related(
                "facility"
            ).filter(**adjusted_filters).values(
                "branchId", "branchName", "branchAddress", "facility_id", "createdAt",
                'facility__facilityName'
            ).order_by("createdAt")
            
            # branches = paginator.paginate_queryset(queryset=branches, request=request)
            return [BranchResponseDTO.transform_branch(branch) for branch in branches]
        except DatabaseError as ex:
            logger.error(f"Database error while fetching branches: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to fetch branches.")
        except Exception as ex:
            logger.error(f"Unexpected error while fetching branches: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while fetching branches.")

    @staticmethod
    def update_branch(branch_id, branch_data):
        """Updates the details of an existing branch."""
        try:
            branch = BranchRepository.get_branch_by_id(branch_id=branch_id)
            for field, value in branch_data.items():
                if hasattr(branch, field):  
                    setattr(branch, field, value)
            branch.full_clean()
            branch.save()
            return branch
        except ValidationError as ex:
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while updating branch: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to update branch.")
        except Exception as ex:
            logger.error(f"Unexpected error while updating branch: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while updating branch.")

    @staticmethod
    def delete_branch(branch_id):
        """Deletes a branch record by ID."""
        try:
            branch = BranchRepository.get_branch_by_id(branch_id=branch_id)
            branch.delete()
            return True
        except NotFoundException as ex:
            raise ex
        except IntegrityError as ex:
            logger.error(f"Integrity error while deleting branch: {ex}", exc_info=True)
            raise IntegrityException(message=ex)
        except DatabaseError as ex:
            logger.error(f"Database error while deleting branch: {ex}", exc_info=True)
            raise QueryException(message="Error executing query to delete branch.")
        except Exception as ex:
            logger.error(f"Unexpected error while deleting branch: {ex}", exc_info=True)
            raise DataBaseException("An unexpected error occurred while deleting branch.")

