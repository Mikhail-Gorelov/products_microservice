from django.urls import path
from . import views

app_name = 'actions'

urlpatterns = [
    path('assessment/', views.AssessmentView.as_view(), name="assessment"),
    path('assessment/show/', views.AssessmentShowView.as_view(), name="assessment-show"),
]
