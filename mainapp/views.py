from django.shortcuts import render, redirect
from django.contrib import messages
from .models import BusinessUnit, Submission
from userauth.models import Account
from django.contrib.auth.decorators import login_required
from utils.decorator import login_required_message
from utils.email_sender import send_mail
from utils.status_updater import update_status
import os
from dotenv import load_dotenv

# Create your views here.
def index(request):
    bussiness_units = BusinessUnit.objects.all()
    idea_champions = Account.objects.filter(is_IC=True)
    
    context = {
        'is_HOMEPAGE':1,
        'bussiness_units':bussiness_units,
        'idea_champions':idea_champions,
    }
    if request.user.is_authenticated:
        if request.user.is_admin:
            return render(request, 'mainapp/admin/home.html', context)
        elif request.user.is_IC:
            if request.method == 'POST':
                data = request.POST
                id = data["submission_id"]
                status_txt = data["status"]

                code = update_status(id, status_txt)
                if code == 1:
                    messages.info(request, 'Status updated successfully!')

                return redirect('home')

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

        load_dotenv()
        send_mail(idea_champion_email, f"New Submission received in BU - {business_unit.name}", f"Hey {business_unit.idea_champion.fullname}! There is a new submission in the business unit {business_unit.name}. Check it out here {os.getenv('WEB_URL')}")
        send_mail(ideator_email, f"Your Submission has been received.", f"Hey {ideator.fullname}! Your submission in the business unit {business_unit.name} has been received. Check the status here {os.getenv('WEB_URL')}/#YOUR_SUBMISSIONS")

        messages.info(request, 'Idea submitted successfully!')
        return redirect('home')

    
    bussiness_units = BusinessUnit.objects.all()
    context = {
        'bussiness_units':bussiness_units,
    }
    return render(request, 'mainapp/ideator/submission_form.html', context)

def all(request):
    if request.method == 'POST':
        data = request.POST
        id = data["submission_id"]
        status_txt = data["status"]

        code = update_status(id, status_txt)
        if code == 1:
            messages.info(request, 'Status updated successfully!')
            
        return redirect('all')

    business_unit = BusinessUnit.objects.get(idea_champion=request.user)
    submissions = Submission.objects.filter(business_unit=business_unit )

    context = {}
    context['business_unit'] = business_unit
    context['submissions'] = submissions

    return render(request, 'mainapp/idea_champion/all.html', context)

def onhold(request):
    if request.method == 'POST':
        data = request.POST
        id = data["submission_id"]
        status_txt = data["status"]

        code = update_status(id, status_txt)
        if code == 1:
            messages.info(request, 'Status updated successfully!')
            
        return redirect('onhold')
    business_unit = BusinessUnit.objects.get(idea_champion=request.user)
    submissions = Submission.objects.filter(business_unit=business_unit )
    onhold_submissions = submissions.filter(status="On Hold")

    context = {}
    context['business_unit'] = business_unit
    context['onhold_submissions'] = onhold_submissions

    return render(request, 'mainapp/idea_champion/onhold.html', context)

def accepted(request):
    if request.method == 'POST':
        data = request.POST
        id = data["submission_id"]
        status_txt = data["status"]
        code = update_status(id, status_txt)
        if code == 1:
            messages.info(request, 'Status updated successfully!')
            
        return redirect('accepted')
    business_unit = BusinessUnit.objects.get(idea_champion=request.user)
    submissions = Submission.objects.filter(business_unit=business_unit )
    accepted_submissions = submissions.filter(status="Accepted")


    context = {}
    context['business_unit'] = business_unit
    context['accepted_submissions'] = accepted_submissions

    return render(request, 'mainapp/idea_champion/accepted.html', context)

def rejected(request):
    if request.method == 'POST':
        data = request.POST
        id = data["submission_id"]
        status_txt = data["status"]

        code = update_status(id, status_txt)
        if code == 1:
            messages.info(request, 'Status updated successfully!')
            
        return redirect('rejected')
    business_unit = BusinessUnit.objects.get(idea_champion=request.user)
    submissions = Submission.objects.filter(business_unit=business_unit )
    rejected_submissions = submissions.filter(status="Rejected")

    context = {}
    context['business_unit'] = business_unit
    context['rejected_submissions'] = rejected_submissions

    return render(request, 'mainapp/idea_champion/rejected.html', context)

from django.http import HttpResponse
def add_BU(request):
    return HttpResponse("Add BU page")

def invite_IC(request):
    return HttpResponse("Invite IC page")
