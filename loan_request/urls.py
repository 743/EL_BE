from django.urls import path

from loan_request import views

urlpatterns = [
    path("loan_request", views.LoanRequestView.as_view(), name="loan-request"),
]
