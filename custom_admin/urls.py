from django.urls import path # type: ignore
from custom_admin.views.appointment_views import *
from custom_admin.views.assessment_views import *
from custom_admin.views.branch_views import *
from custom_admin.views.chart_data_views import *
from custom_admin.views.chart_views import *
from custom_admin.views.facility_views import *
from custom_admin.views.grocery_views import *
from custom_admin.views.incident_views import *
from custom_admin.views.late_submission_views import *
from custom_admin.views.leave_views import *
from custom_admin.views.medication_admin_views import *
from custom_admin.views.medication_views import *
from custom_admin.views.patient_manager_views import *
from custom_admin.views.patient_views import *
from custom_admin.views.update_views import *
from custom_admin.views.utility_views import *
from custom_admin.views.vital_views import *

urlpatterns=[
    path(
        'facilities',
        FacilityView.as_view(), 
        name='facilities'
    ),
    path(
        'facilities/<int:facilityId>',
        FacilityQueryByIDView.as_view(), 
        name='facility-details'
    ),
    

    path(
        'branches',
        BranchView.as_view(), 
        name='branches'
    ),
    path(
        'branches/<int:branchId>',
        BranchQueryByIDView.as_view(), 
        name='branch-details'
    ),


    path(
        'patients',
        PatientView.as_view(), 
        name='patients'
    ),
    path(
        'patients/<int:patientId>',
        PatientQueryByIDView.as_view(), 
        name='patient-details'
    ),


    path(
        'charts-data',
        ChartDataView.as_view(), 
        name='charts-data'
    ),
    path(
        'charts-data/<int:chartDataId>',
        ChartDataQueryByIDView.as_view(), 
        name='charts-data-details'
    ),


    path(
        'charts',
        ChartView.as_view(), 
        name='charts'
    ),
    path(
        'charts/<int:chartId>',
        ChartQueryByIDView.as_view(), 
        name='charts-details'
    ),


    path(
        'medications',
        MedicationView.as_view(), 
        name='medications'
    ),
    path(
        'medications/<int:medicationId>',
        MedicationQueryByIDView.as_view(), 
        name='medication-details'
    ),

    path(
        'medication-administrations',
        MedicationAdministrationView.as_view(), 
        name='medication-administrations'
    ),
    path(
        'medication-administrations/<int:administrationId>',
        MedicationAdministrationQueryByIDView.as_view(), 
        name='medication-administration-details'
    ),


    path(
        'updates',
        UpdateView.as_view(), 
        name='updates'
    ),
    path(
        'updates/<int:updateId>',
        UpdateQueryByIDView.as_view(), 
        name='update-details'
    ),

    path(
        'patient-managers',
        PatientManagerView.as_view(), 
        name='patient-managers'
    ),
    path(
        'patient-managers/<int:managerId>',
        PatientManagerQueryByIDView.as_view(), 
        name='patient-manager-details'
    ),

    path(
        'appointments',
        AppointmentView.as_view(), 
        name='appointments'
    ),
    path(
        'appointments/<int:appointmentId>',
        AppointmentQueryByIDView.as_view(), 
        name='appointment-details'
    ),

    path(
        'vitals',
        VitalView.as_view(), 
        name='vitals'
    ),
    path(
        'vitals/<int:vitalId>',
        VitalQueryByIDView.as_view(), 
        name='vital-details'
    ),


    path(
        'late-submissions',
        LateSubmissionView.as_view(), 
        name='late-submissions'
    ),
    path(
        'late-submissions/<int:submissionId>',
        LateSubmissionQueryByIDView.as_view(), 
        name='late-submission-details'
    ),

    path(
        'leaves',
        LeaveView.as_view(), 
        name='leaves'
    ),
    path(
        'leaves/<int:leaveId>',
        LeaveQueryByIDView.as_view(), 
        name='leave-details'
    ),

    path(
        'utilities',
        UtilityView.as_view(), 
        name='utilities'
    ),
    path(
        'utilities/<int:utilityId>',
        UtilityQueryByIDView.as_view(), 
        name='utility-details'
    ),

    path(
        'groceries',
        GroceryView.as_view(), 
        name='groceries'
    ),
    path(
        'groceries/<int:groceryId>',
        GroceryQueryByIDView.as_view(), 
        name='grocery-details'
    ),

    path(
        'incidents',
        IncidentView.as_view(), 
        name='incidents'
    ),
    path(
        'incidents/<int:incidentId>',
        IncidentQueryByIDView.as_view(), 
        name='incident-details'
    ),

    path(
        'assessments',
        AssessmentView.as_view(), 
        name='assessments'
    ),
    path(
        'assessments/<int:assessmentId>',
        AssessmentQueryByIDView.as_view(), 
        name='assessment-details'
    ),
    path(
        'notifications',
        AssessmentNotificationSchedulerView.as_view(), 
        name='notification-details'
    ),

]