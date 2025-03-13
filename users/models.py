from django.db import models # type: ignore
from django.utils.translation import gettext_lazy as gtl # type: ignore
from phonenumber_field.modelfields import PhoneNumberField # type: ignore
from django.contrib.auth.models import AbstractUser, Group, Permission  # type: ignore
# from custom_admin.models.branch import Branch


class User(AbstractUser):
    """
    - User shared fields
    """
    username = models.CharField(
        max_length=255,
        unique=True,
        error_messages={"unique": gtl("A user with that username already exists.")}
    )
    password = models.CharField(max_length=255)
    avatar = models.FileField(null=True, blank=True, upload_to="resources", default=None)
    firstName = models.CharField(max_length=255)
    middleNames = models.CharField(max_length=255, null=True, blank=True)
    lastName = models.CharField(max_length=255)
    branch = models.ForeignKey(
		"custom_admin.Branch",
		null=True,
		blank=True,
        default=None,
		on_delete=models.SET_NULL,
		related_name='users'
	)
    email = models.EmailField(
        unique=True,
        error_messages={"unique": gtl("A user with that email already exists.")}
    )
    phoneNumber = PhoneNumberField(
        unique=True,
        error_messages={"unique": gtl("A user with the provided phone number already exists")},
        help_text=gtl("Enter a valid phone number"),
    )
    SEX_CHOICES = [('male', 'Male'), ('female', 'Female'), ('other', 'Other Sex')]
    sex = models.CharField(max_length=6, choices=SEX_CHOICES)
    ROLE_CHOICES = [
        ('care giver', 'Care Giver'),
        ('manager', 'Manager'),
        ("superuser", "Super User")
    ]
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('blocked', 'Blocked')
    ]
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='active')
    dateOfBirth = models.DateField(null=True, default=None)
    maritalStatus = models.CharField(max_length=255, null=True, blank=True, default=None)
    position = models.CharField(max_length=255, null=True, default=None, blank=True)
    credential = models.CharField(max_length=255, null=True, blank=True, default=None)
    CRED_STATUS_CHOICES =[
        ('active', 'Active'),
        ('inactive', 'Inactive')
    ]
    credentialStatus = models.CharField(max_length=50, choices=CRED_STATUS_CHOICES, default='active')
    dateEmployed = models.DateField(null=True, default=None)
    supervisor = models.CharField(max_length=255, null=True, blank=True, default=None)
    provider = models.CharField(max_length=255, null=True, blank=True, default=None)
    EMPLOYMENT_STATUS_CHOICES =[
        ('active', 'Active'),
        ('resigned', 'Resigned'),
        ('dismissed', 'Dismissed')
    ]
    
    employmentStatus = models.CharField(max_length=50, choices=EMPLOYMENT_STATUS_CHOICES, default='active')

    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)

    groups = models.ManyToManyField(Group, related_name="custom_user_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="custom_user_permissions", blank=True)


    @classmethod
    def create_user(cls, validated_data):
        """Creates a new user instance from the validated data and hashes the password"""
        password = validated_data.pop("password")
        new_user = cls(**validated_data)
        new_user.set_password(password)
        return new_user
