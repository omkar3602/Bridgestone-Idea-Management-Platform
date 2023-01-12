from django.shortcuts import render, redirect
from django.contrib import messages
from .models import BusinessUnit, Submission
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
            business_unit = BusinessUnit.objects.get(idea_champion=request.user)
            submissions = Submission.objects.filter(business_unit=business_unit )
            pending_submissions = submissions.filter(status="Review Pending")

            context['business_unit'] = business_unit
            context['pending_submissions'] = pending_submissions

            return render(request, 'mainapp/idea_champion/home.html', context)
        else:
            submissions = Submission.objects.filter(ideator=request.user)
            
            context['submissions'] = submissions
            return render(request, 'mainapp/ideator/home.html', context)
    else:
        return render(request, 'mainapp/index.html', context)

@login_required_message(message="Please log in, in order to view the requested page.")
@login_required
def new_submission(request):
    if request.method == 'POST':
        data = request.POST
        name = data['idea_title']
        business_unit_txt = data['business_unit']
        description = data['idea_details']

        ideator = request.user
        business_unit = BusinessUnit.objects.get(name=business_unit_txt)

        submission = Submission(name=name, description=description, business_unit=business_unit, ideator=ideator)
        submission.save()


        idea_champion_email = business_unit.idea_champion.email
        ideator_email = ideator.email

        send_mail(idea_champion_email, f"New Submission received in BU - {business_unit.name}", f"Hey {business_unit.idea_champion.fullname}! There is a new submission in the business unit {business_unit.name}. Check it out here http://127.0.0.1:8000/")
        send_mail(ideator_email, f"Your Submission has been received.", f"Hey {ideator.fullname}! Your submission in the business unit {business_unit.name} has been received. Check the status here http://127.0.0.1:8000/#YOUR_SUBMISSIONS")

        messages.info(request, 'Idea submitted successfully!')
        return redirect('home')

    
    bussiness_units = BusinessUnit.objects.all()
    context = {
        'bussiness_units':bussiness_units,
    }
    return render(request, 'mainapp/ideator/submission_form.html', context)

def onhold(request):
    business_unit = BusinessUnit.objects.get(idea_champion=request.user)
    submissions = Submission.objects.filter(business_unit=business_unit )
    onhold_submissions = submissions.filter(status="On Hold")

    context = {}
    context['business_unit'] = business_unit
    context['onhold_submissions'] = onhold_submissions

    return render(request, 'mainapp/idea_champion/onhold.html', context)

def accepted(request):
    business_unit = BusinessUnit.objects.get(idea_champion=request.user)
    submissions = Submission.objects.filter(business_unit=business_unit )
    accepted_submissions = submissions.filter(status="Accepted")


    context = {}
    context['business_unit'] = business_unit
    context['accepted_submissions'] = accepted_submissions

    return render(request, 'mainapp/idea_champion/accepted.html', context)

def rejected(request):
    business_unit = BusinessUnit.objects.get(idea_champion=request.user)
    submissions = Submission.objects.filter(business_unit=business_unit )
    rejected_submissions = submissions.filter(status="Rejected")

    context = {}
    context['business_unit'] = business_unit
    context['rejected_submissions'] = rejected_submissions

    return render(request, 'mainapp/idea_champion/rejected.html', context)

