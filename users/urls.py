from django.urls import path
from .apis import ListInstitutes, ListExpertise, ListInterests, ListProfiles, SendMessage
from .forgot_password_view import ForgotPasswordView

urlpatterns = [
    path('institute/<int:country>', ListInstitutes.as_view(), name="list-institutes"),
    path('expertises', ListExpertise.as_view(), name="list-expertise"),
    path('interests', ListInterests.as_view(), name="list-interest"),
    path('profiles', ListProfiles.as_view(), name="list-profiles"),
    path('send-message', SendMessage.as_view(), name="send-message")

]
