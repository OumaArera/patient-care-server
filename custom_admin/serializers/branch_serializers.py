from custom_admin.models.branch import Branch
from custom_admin.models.facility import Facility
from rest_framework import serializers # type: ignore

class BranchSerializer(serializers.ModelSerializer):
    """Deserializer for creating a Branch."""
    
    branchAddress = serializers.CharField(required=True)
    facility = serializers.PrimaryKeyRelatedField(queryset=Facility.objects.all())
    email = serializers.EmailField(required=True)
    phoneNumber = serializers.CharField(required=True)
    fax = serializers.CharField(required=True)

    class Meta:
        model = Branch
        fields = ["facility", "branchName", "branchAddress", 'phoneNumber', 'email', 'fax']





class BranchUpdateSerializer(serializers.ModelSerializer):
    """Deserializer for updating a Branch."""
    
    branchAddress = serializers.CharField(required=False)
    facility = serializers.PrimaryKeyRelatedField(queryset=Facility.objects.all(), required=False)
    branchName = serializers.CharField(required=False)
    email = serializers.EmailField(required=False)
    phoneNumber = serializers.CharField(required=False)
    fax = serializers.CharField(required=False)

    class Meta:
        model = Branch
        fields = ["facility", "branchName", "branchAddress", 'phoneNumber', 'email', 'fax']

