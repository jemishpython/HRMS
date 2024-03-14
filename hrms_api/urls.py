from django.urls import path

from . import views


urlpatterns = [

    path("interviewer/aptitude-test/<int:id>", views.AptitudeTest, name='AdminAptitudeTest'),
    path("interviewer/aptitude-test-data/<int:id>", views.AptitudeTestData, name='AdminAptitudeTestData'),
]