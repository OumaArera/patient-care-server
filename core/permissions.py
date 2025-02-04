from rest_framework.permissions import BasePermission # type: ignore
from users.repository import UserRepository

class RolePermission(BasePermission):
	"""
	Custom permission to allow access based on user roles.
	"""
	allowed_roles = []
	
	def add_roles(self, roles):
		if not isinstance(roles, list):
			raise ValueError("Roles must be provided as a list.")
		self.allowed_roles = list(set(self.allowed_roles + roles))
	
	def has_permission(self, request, view):
		return bool(
			request.user
			and  request.user.is_authenticated
			and request.user.role in self.allowed_roles
		)
	
class IsSuperUser(BasePermission):
	"""Custom permission class to allow access only to superusers."""
	
	def has_permission(self, request, view):
		"""Check if the user is authenticated and is a superuser"""
		if UserRepository.check_if_superuser_exists() and request.user and request.user.is_authenticated and request.user.is_superuser:
			
			return True
		elif not UserRepository.check_if_superuser_exists():
			return True
		else:
			return False
		
class IsCareGiver(RolePermission):
	"""
	Permission to allow care givers to update their own details.
	"""
	allowed_roles = [
		'care giver', 'superuser'
	]
	def add_roles(self, allowed_roles):
		return super().add_roles(allowed_roles)
	
class IsManager(RolePermission):
	"""
	Permission to allow managers to update their own details.
	"""
	allowed_roles = [
		'manager', 'superuser'
	]
	def add_roles(self, allowed_roles):
		return super().add_roles(allowed_roles)
	
class IsAllUsers(RolePermission):
	"""
	Permission to allow managers to update their own details.
	"""
	allowed_roles = [
		'manager', 'superuser', 'care giver'
	]
	def add_roles(self, allowed_roles):
		return super().add_roles(allowed_roles)