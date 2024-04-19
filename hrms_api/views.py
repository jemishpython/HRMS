import datetime
import pytz
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect

from hrms_api.choices import GroupMembertypeChoice
from hrms_api.forms import GroupChatForm, AddGroupMemberForm
from hrms_api.models import Interviewers, InterviewQuestions, InterviewerResult, User, PersonalConversation, \
    PersonalConversationMessage, GroupConversation, GroupConversationMessage, GroupMember


# Create your views here.


def AptitudeTest(request, id, technology, token):
    interviewer_details = Interviewers.objects.get(id=id)

    current_time = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))

    if interviewer_details.token_created_at < current_time - datetime.timedelta(seconds=310):
        interviewer_details.aptitude_test_token = None
        interviewer_details.save()
        return redirect('QuizLinkExpire', id=id)

    interview_question_list = InterviewQuestions.objects.filter(technology=technology).order_by('?')[:10]
    context = {
        'interview_question_list': interview_question_list,
        'interviewer_details': interviewer_details,
    }
    return render(request, 'admin/aptitude_test.html', context)


def AptitudeTestData(request, id):
    interviewer_detail = Interviewers.objects.get(id=id)
    technology_id = interviewer_detail.technology
    if request.method == 'POST':
        try:
            user_answer_list = []
            interview_question_ids = [int(key.split('_')[-1]) for key in request.POST if key.startswith('user_answer_')]
            interview_question_list = InterviewQuestions.objects.filter(technology=technology_id, id__in=interview_question_ids)
            for question in interview_question_list:
                user_answer = request.POST.get('user_answer_' + str(question.id), '')
                user_answer_list.append(user_answer)

                result = InterviewerResult(interviewer=interviewer_detail, question=question, user_answer=user_answer)
                result.save()

            score = sum(user_answer_list[i] == question.answer for i, question in enumerate(interview_question_list))

            interviewer_detail.result = str(score)
            interviewer_detail.save()
            messages.success(request, 'Your test submit successfully')
            return redirect('ThankYouPage')
        except Exception as e:
            messages.error(request, f"ERROR : {e}")
    return render(request, "admin/aptitude_test.html", {'interviewer_details': interviewer_detail, 'technology': technology_id})


def ThankYouPage(request):
    return render(request, 'aptitude_test_thankyou_page.html')


def QuizLinkExpire(request, id):
    interviewer_details = Interviewers.objects.get(id=id)
    return render(request, 'admin/quiz_link_expire.html', {'interviewer_details': interviewer_details})


@login_required(login_url="Login")
def ChatView(request):
    user = request.user
    user_list = User.objects.all()
    group_list = GroupMember.objects.filter(member=user.id)
    context = {
        'user_list': user_list,
        'group_list': group_list,
    }
    return render(request, "admin/chat.html", context)


@login_required(login_url="Login")
def Chat(request, userID):
    sender_id = request.user.id
    sender = User.objects.get(id=sender_id)
    group_list = GroupMember.objects.filter(member=sender_id)
    user_list = User.objects.all()
    chat_users = User.objects.get(id=userID)
    current_time = datetime.datetime.now()

    PersonalConversation.create_if_not_exists(sender_id, chat_users.id)

    room_name = PersonalConversation.chat_conversation_exists(sender_id, chat_users.id)

    old_messages = PersonalConversationMessage.objects.filter(conversation=room_name.id).order_by('timestamp')

    context = {
        'chat_users': chat_users,
        'user_list': user_list,
        'room_name': room_name.id,
        'massages': old_messages,
        'sender': sender,
        'current_time': current_time,
        'group_list': group_list,
    }
    return render(request, "admin/chat.html", context)


@login_required(login_url="Login")
def GroupChatCreate(request):
    user = request.user.id
    admin_user = User.objects.get(id=user)
    form = GroupChatForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        try:
            if form.is_valid():
                add_chat_group = form.save(commit=False)
                add_chat_group.save()

                group_member, created = GroupMember.objects.get_or_create(group=add_chat_group, member=admin_user, member_type=GroupMembertypeChoice.ADMIN)
                group_member.save()

                messages.success(request, 'Group create successfully')
                return redirect('ChatView')
            else:
                messages.error(request, f"Form Not Valid : {form.errors}")
        except Exception as e:
            messages.error(request, f"ERROR : {e}")

    context = {'form': form}
    return render(request, "admin/add_chat_group.html", context)


@login_required(login_url="Login")
def AddGroupChatMember(request, id):
    group_id = GroupConversation.objects.get(pk=id)
    form = AddGroupMemberForm(request.POST or None)
    if request.method == 'POST':
        try:
            # if form.is_valid():
            selected_users = form.data.getlist('member')
            for user_id in selected_users:
                user = User.objects.get(id=user_id)
                group_member, created = GroupMember.objects.get_or_create(group=group_id, member=user)
                if created:
                    group_member.save()

            messages.success(request, 'Group create successfully')
            return redirect('GroupChat', groupID=group_id.id)
            # else:
            #     print(">>>>>>>>>>>>>>>>>>>>>> FORM ERROR : ",form.errors)
            #     messages.error(request, "FORM ERROR : ", form.errors)
        except Exception as e:
            messages.error(request, f"ERROR : {e}")

    context = {'form': form, 'group_id': group_id}
    return render(request, "admin/add_chat_group_member.html", context)


@login_required(login_url="Login")
def GroupChat(request, groupID):
    user = request.user
    group_details = GroupConversation.objects.get(pk=groupID)
    group_list = GroupMember.objects.filter(member=user.id)
    sender_id = request.user.id
    sender = User.objects.get(id=sender_id)
    user_list = User.objects.all()
    group_member = GroupMember.objects.filter(group=group_details.id)
    current_time = datetime.datetime.now()

    old_messages = GroupConversationMessage.objects.filter(conversation__group=group_details.id).order_by('timestamp')

    context = {
        'user_list': user_list,
        'group_member': group_member,
        'group_details': group_details,
        'group_room_name': group_details.id,
        'massages': old_messages,
        'sender': sender,
        'current_time': current_time,
        'group_list': group_list,
    }
    return render(request, "admin/chat.html", context)


@login_required(login_url="EmployeeLogin")
def EmpChatView(request):
    user = request.user
    user_list = User.objects.all()
    group_list = GroupMember.objects.filter(member=user.id)
    context = {
        'user_list': user_list,
        'group_list': group_list,
    }
    return render(request, "employee/chat.html", context)


@login_required(login_url="EmployeeLogin")
def EmpChat(request, userID):
    sender_id = request.user.id
    sender = User.objects.get(id=sender_id)
    group_list = GroupMember.objects.filter(member=sender_id)
    user_list = User.objects.all()
    chat_users = User.objects.get(id=userID)
    current_time = datetime.datetime.now()

    PersonalConversation.create_if_not_exists(sender_id, chat_users.id)

    room_name = PersonalConversation.chat_conversation_exists(sender_id, chat_users.id)

    old_messages = PersonalConversationMessage.objects.filter(conversation=room_name.id).order_by('timestamp')

    context = {
        'chat_users': chat_users,
        'user_list': user_list,
        'room_name': room_name.id,
        'massages': old_messages,
        'sender': sender,
        'current_time': current_time,
        'group_list': group_list,
    }
    return render(request, "employee/chat.html", context)


@login_required(login_url="EmployeeLogin")
def EmpGroupChatCreate(request):
    user = request.user.id
    admin_user = User.objects.get(id=user)
    form = GroupChatForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        try:
            if form.is_valid():
                add_chat_group = form.save(commit=False)
                add_chat_group.save()

                group_member, created = GroupMember.objects.get_or_create(group=add_chat_group, member=admin_user,member_type=GroupMembertypeChoice.ADMIN)
                group_member.save()

                messages.success(request, 'Group create successfully')
                return redirect('EmpChatView')
            else:
                messages.error(request, f"Form Not Valid : {form.errors}")
        except Exception as e:
            messages.error(request, f"ERROR : {e}")

    context = {'form': form}
    return render(request, "employee/add_chat_group.html", context)


@login_required(login_url="EmployeeLogin")
def AddEmpGroupChatMember(request, id):
    group_id = GroupConversation.objects.get(pk=id)
    form = AddGroupMemberForm(request.POST or None)
    if request.method == 'POST':
        try:
            # if form.is_valid():
            selected_users = form.data.getlist('member')
            for user_id in selected_users:
                user = User.objects.get(id=user_id)
                group_member, created = GroupMember.objects.get_or_create(group=group_id, member=user)
                if created:
                    group_member.save()

            messages.success(request, 'Group create successfully')
            return redirect('EmpGroupChat', groupID=group_id.id)
            # else:
            #     print(">>>>>>>>>>>>>>>>>>>>>> FORM ERROR : ",form.errors)
            #     messages.error(request, "FORM ERROR : ", form.errors)
        except Exception as e:
            messages.error(request, f"ERROR : {e}")

    context = {'form': form, 'group_id': group_id}
    return render(request, "employee/add_chat_group_member.html", context)


@login_required(login_url="EmployeeLogin")
def EmpGroupChat(request, groupID):
    user = request.user
    group_details = GroupConversation.objects.get(pk=groupID)
    group_list = GroupMember.objects.filter(member=user.id)
    sender_id = request.user.id
    sender = User.objects.get(id=sender_id)
    user_list = User.objects.all()
    group_member = GroupMember.objects.filter(group=group_details.id)
    current_time = datetime.datetime.now()

    old_messages = GroupConversationMessage.objects.filter(conversation__group=group_details.id).order_by('timestamp')

    context = {
        'user_list': user_list,
        'group_member': group_member,
        'group_details': group_details,
        'group_room_name': group_details.id,
        'massages': old_messages,
        'sender': sender,
        'current_time': current_time,
        'group_list': group_list,
    }
    return render(request, "employee/chat.html", context)
