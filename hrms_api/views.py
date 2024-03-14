from django.contrib import messages
from django.shortcuts import render, redirect
from hrms_api.forms import AptitudeTestForm
from hrms_api.models import Interviewers, InterviewQuestions


# Create your views here.


def AptitudeTest(request, id):
    interviewer_details = Interviewers.objects.get(id=id)
    interview_question_list = InterviewQuestions.objects.all()
    context = {
        'interview_question_list': interview_question_list,
        'interviewer_details': interviewer_details,
    }
    return render(request, 'admin/aptitude_test.html', context)


def AptitudeTestData(request, id):
    interviewer_detail = Interviewers.objects.get(id=id)
    form = AptitudeTestForm(request.POST or None)
    if request.method == 'POST':
        try:
            if form.is_valid():
                test_data = form.save(commit=False)
                test_data.user_name = interviewer_detail
                test_data.save()
                selected_questions = request.POST.getlist('question')
                selected_answers = request.POST.getlist('answer')
                messages.success(request, 'Your test submit successfully')
                return redirect('AdminInterviewQuestion')
            else:
                messages.error(request, f"Form Not Valid : {form.errors}")
        except Exception as e:
            messages.error(request, f"ERROR : {e}")
    return render(request, "admin/interview-dashboard.html")