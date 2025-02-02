from custom_admin.models.branch import Branch
from custom_admin.models.facility import Facility
from rest_framework import serializers # type: ignore
from django.core.validators import RegexValidator  # type: ignore

class BranchSerializer(serializers.ModelSerializer):
    """Deserializer for creating a Branch."""
    
    branchAddress = serializers.CharField(
        required=True,
        validators=[
            RegexValidator(
                regex=r"^\d+\s[A-Za-z\s]+,\s[A-Za-z\s]+,\s[A-Z]{2}\s\d{5}(-\d{4})?$",
                message="Invalid address format. Expected format: '123 Main St, Springfield, IL 62704' "
                        "or '456 Elm Ave, New York, NY 10001-2345'"
            )
        ]
    )
    facility = serializers.PrimaryKeyRelatedField(queryset=Facility.objects.all())

    class Meta:
        model = Branch
        fields = ["facility", "branchName", "branchAddress"]




class BranchUpdateSerializer(serializers.ModelSerializer):
    """Deserializer for updating a Branch."""
    
    branchAddress = serializers.CharField(
        required=False,
        validators=[
            RegexValidator(
                regex=r"^\d+\s[A-Za-z\s]+,\s[A-Za-z\s]+,\s[A-Z]{2}\s\d{5}(-\d{4})?$",
                message="Invalid address format. Expected format: '123 Main St, Springfield, IL 62704' "
                        "or '456 Elm Ave, New York, NY 10001-2345'"
            )
        ]
    )
    facility = serializers.PrimaryKeyRelatedField(queryset=Facility.objects.all(), required=False)
    branchName = serializers.CharField(required=False)

    class Meta:
        model = Branch
        fields = ["facility", "branchName", "branchAddress"]