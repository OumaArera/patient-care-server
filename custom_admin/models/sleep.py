from django.db import models
from custom_admin.models import Patient


class Sleep(models.Model):
    """Sleep pattern reporting"""
    sleepId = models.AutoField(primary_key=True)
    resident =  models.ForeignKey(
      Patient,
      null=True,
      blank=True,
      on_delete=models.SET_NULL,
      related_name='sleeps'
    )
    SLEEP_CHOICES =[
        ("A", "Awake"), 
        ("S", "Sleeping")
    ]
    markAs = models.CharField(max_length=50, choices=SLEEP_CHOICES)
    dateTaken = models.DateField()
    TIME_CHOICES = [
        ("7:00AM", "7:00 AM"),
        ("8:00AM", "8:00 AM"),
        ("9:00AM", "9:00 AM"),
        ("10:00AM", "10:00 AM"),
        ("11:00AM", "11:00 AM"),
        ("12:00PM", "12:00 PM (Noon)"),
        ("1:00PM", "1:00 PM"),
        ("2:00PM", "2:00 PM"),
        ("3:00PM", "3:00 PM"),
        ("4:00PM", "4:00 PM"),
        ("5:00PM", "5:00 PM"),
        ("6:00PM", "6:00 PM"),
        ("7:00PM", "7:00 PM"),
        ("8:00PM", "8:00 PM"),
        ("9:00PM", "9:00 PM"),
        ("10:00PM", "10:00 PM"),
        ("11:00PM", "11:00 PM"),
        ("12:00AM", "12:00 AM (Midnight)"),
        ("1:00AM", "1:00 AM"),
        ("2:00AM", "2:00 AM"),
        ("3:00AM", "3:00 AM"),
        ("4:00AM", "4:00 AM"),
        ("5:00AM", "5:00 AM"),
        ("6:00AM", "6:00 AM"),
    ]
    reasonFilledLate = models.TextField(null=True, blank=True, default=None)
    markedFor = models.CharField(max_length=50, choices=TIME_CHOICES)
    createdAt = models.DateTimeField(auto_now_add=True)
    modifiedAt = models.DateTimeField(auto_now=True)

    @classmethod
    def create_sleep_entry(cls, validated_data):
        """
        Create a new sleep instance from validated data.
        """
        new_sleep = cls(**validated_data)
        return new_sleep