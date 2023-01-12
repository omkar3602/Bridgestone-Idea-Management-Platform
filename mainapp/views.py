from django.shortcuts import render
from .models import BusinessUnit
from userauth.models import Account
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from utils.decorator import login_required_message
from utils.email_sender import send_mail

# Create your views here.
def index(request):
    bussiness_units = BusinessUnit.objects.all()
    idea_champions = Account.objects.filter(is_IC=True)

    context = {
        'bussiness_units':bussiness_units,
        'idea_champions':idea_champions,
    }
    if request.user.is_authenticated:
        if request.user.is_admin:
            return HttpResponse("Admin home page")
        elif request.user.is_IC:
            return HttpResponse("IC home page")
        else:
            return render(request, 'mainapp/ideator/home.html', context)
    else:
        return render(request, 'mainapp/index.html', context)

@login_required_message(message="Please log in, in order to view the requested page.")
@login_required
def new_submission(request):
    if request.method == 'POST':
        data = request.POST
        idea_title = data['idea_title']
        business_unit = data['business_unit']
        idea_details = data['idea_details']
        print(data)
    
    bussiness_units = BusinessUnit.objects.all()
    context = {
        'bussiness_units':bussiness_units,
    }
    return render(request, 'mainapp/ideator/submission_form.html', context)


# @login_required
# def send_email(request):
#     if request.method == 'POST':
#         data = request.POST
#         receiver_email = data['email']
#         sender_name = data['sender_name']
#         sender_email = data['sender_email']
#         subject_name = data['subject_name']
#         topic_name = data['topic_name']
#         effect_link = data['effect_link']

#         send_mail(receiver_email, sender_name, sender_email, subject_name, topic_name, effect_link)


#         messages.info(request, f'Email sent to {receiver_email}')
#         return redirect('subject', subject_name)
#     return redirect('home')