from django.contrib import messages
from django.shortcuts import render, redirect
from hrms_api.models import Interviewers, InterviewQuestions


# Create your views here.


def AptitudeTest(request, id, technology):
    interviewer_details = Interviewers.objects.get(id=id)
    interview_question_list = InterviewQuestions.objects.filter(technology=technology)
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
            correct_answers = []
            interview_question_list = InterviewQuestions.objects.filter(technology=technology_id)

            for question in interview_question_list:
                user_answer = request.POST.get('user_answer_' + str(question.id), '')
                user_answer_list.append(user_answer)
                correct_answers.append(question.answer)

            score = sum(user_answer_list[i] == correct_answers[i] for i in range(len(user_answer_list)))

            interviewer_detail.result = str(score)
            interviewer_detail.save()
            messages.success(request, 'Your test submit successfully')
            return redirect('ThankYouPage')
        except Exception as e:
            messages.error(request, f"ERROR : {e}")
    return render(request, "admin/aptitude_test.html", {'interviewer_details': interviewer_detail, 'technology': technology_id})


def ThankYouPage(request):
    return render(request, 'thankyou_page.html')
