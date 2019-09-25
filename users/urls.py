from django.urls import path
from .apis import ListInstitutes, ListExpertise, ListInterests, ListProfiles, SendMessage, ListCountries, ListSubjects, Me, RetrieveProfile, ListCiblings
from .apis import UpdateProfilePic , UpdateCoverPic, ListOffer
from .forgot_password_view import ForgotPasswordView

urlpatterns = [
    path('institute/<int:country>', ListInstitutes.as_view(), name="list-institutes"),
    path('expertises', ListExpertise.as_view(), name="list-expertise"),
    path('interests', ListInterests.as_view(), name="list-interest"),
    path('offers', ListOffer.as_view(), name="list-offer"),
    path('profiles', ListProfiles.as_view(), name="list-profiles"),
    path('profile/<str:user>', RetrieveProfile.as_view(), name="list-profiles"),
    path('send-message', SendMessage.as_view(), name="send-message"),
    path('countries', ListCountries.as_view(), name="list-countries"),
    path('subjects', ListSubjects.as_view(), name="list-subjects"),
    path('me', Me.as_view(), name="me"),
    path('ciblings', ListCiblings.as_view(), name="list-ciblings"),
    path('update-profile-img/<int:pk>', UpdateProfilePic.as_view(), name="update-profile-pic"),
    path('update-cover-pic/<int:pk>', UpdateCoverPic.as_view(), name="update-cover-pic")

]
