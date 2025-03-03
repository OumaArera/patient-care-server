from django.db import models # type: ignore
from custom_admin.models.facility import Facility  # type: ignore
from django.core.exceptions import ValidationError # type: ignore

class Branch(models.Model):
    """Create branches"""
    branchId = models.AutoField(primary_key=True)
    facility = models.ForeignKey(
		Facility,
		on_delete=models.CASCADE,
		related_name='branches'
	)
    branchName = models.CharField(max_length=255)
    branchAddress = models.CharField(max_length=255)
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        """Ensure branchName is unique, case insensitive for both creation and updates"""
        if Branch.objects.exclude(pk=self.pk).filter(branchName__iexact=self.branchName).exists():
            raise ValidationError(f"A branch with name '{self.branchName}' already exists.")
        
        super().save(*args, **kwargs)

    @classmethod
    def create_branch(cls, validated_data):
        """
        Create a new branches instance from validated data.
        """
        branch = cls(**validated_data)
        return branch

