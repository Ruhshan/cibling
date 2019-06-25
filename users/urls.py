from django.urls import path
from .apis import ListInstitutes, ListExpertise, ListInterests
from .forgot_password_view import ForgotPasswordView

urlpatterns = [
    path('institute/<int:country>', ListInstitutes.as_view(), name="list-institutes"),
    path('expertises', ListExpertise.as_view(), name="list-expertise"),
    path('interests', ListInterests.as_view(), name="list-interest"),
    path('forgot-password', ForgotPasswordView.as_view(), name="forgot-password")
]
