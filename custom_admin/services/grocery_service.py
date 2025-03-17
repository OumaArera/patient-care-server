from custom_admin.repositories.grocery_repo import GroceryRepository
from core.dtos.grocery_dto import GroceryResponseDTO

class GroceryService:
    """Handles the business logic for groceries."""

    @staticmethod
    def create_grocery(data):
        """Creates a new grocery entry in the database."""
        try:
            new_grocery = GroceryRepository.create_grocery(grocery_data=data)
            return GroceryResponseDTO.transform_grocery(grocery=new_grocery)
        except Exception as ex:
            raise ex

    @staticmethod
    def get_grocery_by_id(grocery_id):
        """Fetches details of a grocery by ID."""
        try:
            grocery = GroceryRepository.get_grocery_by_id(grocery_id=grocery_id)
            return GroceryResponseDTO.transform_grocery(grocery=grocery)
        except Exception as ex:
            raise ex

    @staticmethod
    def get_all_groceries(query_params):
        """Fetches and returns all groceries with optional filtering."""
        try:
            query_params.pop("pageSize", None)
            query_params.pop("pageNumber", None)
            groceries = GroceryRepository.get_all_groceries(query_params=query_params)
            return groceries
        except Exception as ex:
            raise ex

    @staticmethod
    def update_grocery(grocery_id, grocery_data):
        """Updates an existing grocery entry."""
        try:
            updated_grocery = GroceryRepository.update_grocery(
                grocery_id=grocery_id,
                grocery_data=grocery_data
            )
            return GroceryResponseDTO.transform_grocery(grocery=updated_grocery)
        except Exception as ex:
            raise ex

    @staticmethod
    def delete_grocery(grocery_id):
        """Deletes a grocery entry by ID."""
        try:
            return GroceryRepository.delete_grocery(grocery_id=grocery_id)
        except Exception as ex:
            raise ex
