from django.urls import path
from .apis import ListInstitutes

urlpatterns=[
    path('institute/<int:country>',ListInstitutes.as_view(),name="list-institutes")
]