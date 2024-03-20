import datetime
import pytz
from django.contrib import messages
from django.shortcuts import render, redirect
from hrms_api.models import Interviewers, InterviewQuestions, InterviewerResult


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
    return render(request, 'admin/quiz_link_expire.html', {'interviewer_details':interviewer_details})
