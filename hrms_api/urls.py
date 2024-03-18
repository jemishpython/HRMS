from django.urls import path

from . import views


urlpatterns = [

    path("interviewer/aptitude-test/<int:id>/<int:technology>", views.AptitudeTest, name='AdminAptitudeTest'),
    path("interviewer/aptitude-test-data/<int:id>", views.AptitudeTestData, name='AdminAptitudeTestData'),
    path("interviewer/aptitude-test/rules", views.Rules, name='rules'),

    path("thank_you_page", views.ThankYouPage, name="ThankYouPage"),
]