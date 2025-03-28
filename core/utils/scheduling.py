import logging
from datetime import timedelta, date
from users.models import User
from django.db import models
from core.utils.email_html import EmailHtmlContent
from core.utils.send_email import send_email
from custom_admin.models.assessment import Assessment

logger = logging.getLogger(__name__)

def schedule_email_notifications():
    """Sends email notifications to superusers if an assessment is due in 10 days or less."""
    try:
        today = date.today()
        notification_start_date = today + timedelta(days=10)
        due_assessments = Assessment.objects.filter(
            models.Q(assessmentNextDate__lte=notification_start_date, assessmentNextDate__gte=today) |
            models.Q(NCPNextDate__lte=notification_start_date, NCPNextDate__gte=today)
        )
        print(f"Assessments: {due_assessments}")
        if not due_assessments.exists():
            logger.info("No assessments due for notifications today.")
            return

        superusers = User.objects.filter(role="superuser").all()
        print(f"Superuser: {superusers}")
        if not superusers.exists():
            logger.warning("No superusers found to notify.")
            return

        for assessment in due_assessments:
            resident_name = f"{assessment.resident.firstName} {assessment.resident.lastName}" if assessment.resident else "Unknown Resident"
            branch = assessment.resident.branch.branchName
            socialWorker = assessment.socialWorker
            
            for superuser in superusers:
                assessment_dates = []
                if assessment.assessmentNextDate:
                    assessment_dates.append(f"Assessment Date: {assessment.assessmentNextDate}")
                if assessment.NCPNextDate:
                    assessment_dates.append(f"NCP Date: {assessment.NCPNextDate}")

                assessment_date_str = ", ".join(assessment_dates) if assessment_dates else "No date available"

                html_body = EmailHtmlContent.assessment_notification_html(
                    resident=resident_name,
                    assessment_date=assessment_date_str,
                    recipient=f"{superuser.firstName} {superuser.lastName}",
                    branch=branch,
                    socialWorker =socialWorker
                )
                send_email(
                    recipient_email=superuser.email,
                    recipient_name=f"{superuser.firstName} {superuser.lastName}",
                    subject="Assessment Due Notification",
                    html_content=html_body
                )
                logger.info(f"Notification sent to {superuser.email} for assessment of {resident_name}.")
    except Exception as ex:
        logger.error(f"Unexpected error while scheduling assessment notifications: {ex}", exc_info=True)
