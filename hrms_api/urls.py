from django.urls import path

from . import views


urlpatterns = [

    path("interviewer/aptitude-test/<int:id>/<int:technology>/<uuid:token>", views.AptitudeTest, name='AdminAptitudeTest'),
    path("interviewer/aptitude-test-data/<int:id>", views.AptitudeTestData, name='AdminAptitudeTestData'),
    path("interviewer/aptitude-test/quiz-link-expire/<int:id>", views.QuizLinkExpire, name='QuizLinkExpire'),

    path("thank_you_page", views.ThankYouPage, name="ThankYouPage"),
]
