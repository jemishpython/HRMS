from django.urls import path

from . import views


urlpatterns = [

    path("interviewer/aptitude-test/<int:id>/<int:technology>/<uuid:token>", views.AptitudeTest, name='AdminAptitudeTest'),
    path("interviewer/aptitude-test-data/<int:id>", views.AptitudeTestData, name='AdminAptitudeTestData'),
    path("interviewer/aptitude-test/quiz-link-expire/<int:id>", views.QuizLinkExpire, name='QuizLinkExpire'),

    path("thank_you_page", views.ThankYouPage, name="ThankYouPage"),

    path("chat-view", views.ChatView, name='ChatView'),
    path("chat/group-add", views.GroupChatCreate, name='AddGroupChat'),
    path("chat/<int:userID>", views.Chat, name='Chat'),

    path("group-chat-view", views.ChatView, name='GroupChatView'),
    path("group-chat/<int:userID>", views.Chat, name='GroupChat'),

    path("chat-view/", views.EmpChatView, name='EmpChatView'),
    path("employee/chat/<int:userID>", views.EmpChat, name='EmpChat'),
]
