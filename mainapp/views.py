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
        'selected':'all',
        'bussiness_units':bussiness_units,
        'idea_champions':idea_champions,
    }

    if request.user.is_authenticated:
        if request.user.is_idea_admin:
            graph1_dict = {}
            ideators = Account.objects.filter(is_ideator=True)
            submissions = Submission.objects.all()

            for ideator in ideators:
                graph1_dict[str(ideator.fullname)] = 0
            
            for submission in submissions:
                graph1_dict[str(submission.ideator)] += 1
            context['ideators'] = list(graph1_dict.keys())
            context['submissions'] = list(graph1_dict.values())


            graph2_dict = {}
            business_units = BusinessUnit.objects.all()
            submissions = Submission.objects.all()

            for business_unit in business_units:
                graph2_dict[str(business_unit.name)] = 0
            
            for submission in submissions:
                graph2_dict[str(submission.business_unit)] += 1
            context['business_units'] = list(graph2_dict.keys())
            context['submissions'] = list(graph2_dict.values())

            graph3_dict = {
                "Review Pending":0, 
                "Accepted":0, 
                "Rejected":0, 
                "On Hold":0,
            }
            submissions = Submission.objects.all()
            
            for submission in submissions:
                graph3_dict[str(submission.status)] += 1
            context['submission_status'] = list(graph3_dict.keys())
            context['no_of_submissions'] = list(graph3_dict.values())
            return render(request, 'mainapp/idea_admin/home.html', context)
        elif request.user.is_IC:
            if request.method == 'POST':
                data = request.POST
                id = data["submission_id"]
                status_txt = data["status"]

                code = update_status(id, status_txt)
                if code == 1:
                    messages.info(request, 'Status updated successfully!')

                return redirect('home')

            business_unit = BusinessUnit.objects.filter(idea_champion=request.user)
            if business_unit:
                business_unit = business_unit[0]
                submissions = Submission.objects.filter(business_unit=business_unit )
                pending_submissions = submissions.filter(status="Review Pending")

                context['business_unit'] = business_unit
                context['pending_submissions'] = pending_submissions
            return render(request, 'mainapp/idea_champion/home.html', context)
        elif request.user.is_ideator:
            if request.method == 'POST':
                data = request.POST
                selected = data['selected']
                
                if selected == "all":
                    submissions = Submission.objects.filter(ideator=request.user)
                elif selected == "review_pending":
                    submissions = Submission.objects.filter(ideator=request.user).filter(status="Review Pending")
                elif selected == "accepted":
                    submissions = Submission.objects.filter(ideator=request.user).filter(status="Accepted")
                elif selected == "on_hold":
                    submissions = Submission.objects.filter(ideator=request.user).filter(status="On Hold")
                elif selected == "rejected":
                    submissions = Submission.objects.filter(ideator=request.user).filter(status="Rejected")

                context['submissions'] = submissions
                return render(request, 'mainapp/ideator/home.html', context)
            submissions = Submission.objects.filter(ideator=request.user)
            
            context['submissions'] = submissions
            return render(request, 'mainapp/ideator/home.html', context)
        else:
            return render(request, 'mainapp/index.html', context)
    else:
        return render(request, 'mainapp/index.html', context)

@login_required_message(message="Please log in, in order to view the requested page.")
@login_required
def new_submission(request):
    if request.user.is_ideator == False:
        messages.info(request, "You don't have access to this page.")
        return redirect('home')
    else:
        if request.method == 'POST':
            data = request.POST
            files = request.FILES
            name = data['idea_title']
            business_unit_txt = data['business_unit']
            description = data['idea_details']

            ideator = request.user
            business_unit = BusinessUnit.objects.get(name=business_unit_txt)

            if 'attachment' in files.keys():
                attachment = files['attachment']
                submission = Submission(name=name, description=description, business_unit=business_unit, ideator=ideator, attachment=attachment)
            else:
                submission = Submission(name=name, description=description, business_unit=business_unit, ideator=ideator)
            submission.save()


            idea_champion_email = business_unit.idea_champion.email
            ideator_email = ideator.email

            load_dotenv()
            send_mail(idea_champion_email, f"New Submission received in BU - {business_unit.name}", f"Hey {business_unit.idea_champion.fullname}! There is a new submission in the business unit {business_unit.name}. Check it out here {os.getenv('WEB_URL')}")
            send_mail(ideator_email, f"Your Submission has been received.", f"Hey {ideator.fullname}! Your submission in the business unit {business_unit.name} has been received. Check the status here {os.getenv('WEB_URL')}#YOUR_SUBMISSIONS")

            messages.info(request, 'Idea submitted successfully!')
            return redirect('home')

        bussiness_units = BusinessUnit.objects.all()
        bu_id = request.GET.get('bu_id', '')
        if bu_id != '':
            bu_id = int(bu_id)
        context = {
            'bussiness_units':bussiness_units,
            'bu_id':bu_id,
        }
        return render(request, 'mainapp/ideator/submission_form.html', context)

@login_required_message(message="Please log in, in order to view the requested page.")
@login_required
def all(request):
    if request.user.is_IC == False:
        messages.info(request, "You don't have access to this page.")
        return redirect('home')
    else:
        if request.method == 'POST':
            data = request.POST
            id = data["submission_id"]
            status_txt = data["status"]

            code = update_status(id, status_txt)
            if code == 1:
                messages.info(request, 'Status updated successfully!')
                
            return redirect('all')

        business_unit = BusinessUnit.objects.filter(idea_champion=request.user)
        if business_unit:
            business_unit = business_unit[0]
            submissions = Submission.objects.filter(business_unit=business_unit)

            context = {}
            context['business_unit'] = business_unit
            context['submissions'] = submissions

        return render(request, 'mainapp/idea_champion/all.html', context)

@login_required_message(message="Please log in, in order to view the requested page.")
@login_required
def onhold(request):
    if request.user.is_IC == False:
        messages.info(request, "You don't have access to this page.")
        return redirect('home')
    else:
        if request.method == 'POST':
            data = request.POST
            id = data["submission_id"]
            status_txt = data["status"]

            code = update_status(id, status_txt)
            if code == 1:
                messages.info(request, 'Status updated successfully!')
                
            return redirect('onhold')
        business_unit = BusinessUnit.objects.filter(idea_champion=request.user)
        if business_unit:
            business_unit = business_unit[0]
            submissions = Submission.objects.filter(business_unit=business_unit )
            onhold_submissions = submissions.filter(status="On Hold")

            context = {}
            context['business_unit'] = business_unit
            context['onhold_submissions'] = onhold_submissions

        return render(request, 'mainapp/idea_champion/onhold.html', context)

@login_required_message(message="Please log in, in order to view the requested page.")
@login_required
def accepted(request):
    if request.user.is_IC == False:
        messages.info(request, "You don't have access to this page.")
        return redirect('home')
    else:
        if request.method == 'POST':
            data = request.POST
            id = data["submission_id"]
            status_txt = data["status"]
            code = update_status(id, status_txt)
            if code == 1:
                messages.info(request, 'Status updated successfully!')
                
            return redirect('accepted')
        business_unit = BusinessUnit.objects.filter(idea_champion=request.user)
        if business_unit:
            business_unit = business_unit[0]
            submissions = Submission.objects.filter(business_unit=business_unit )
            accepted_submissions = submissions.filter(status="Accepted")


            context = {}
            context['business_unit'] = business_unit
            context['accepted_submissions'] = accepted_submissions

        return render(request, 'mainapp/idea_champion/accepted.html', context)

@login_required_message(message="Please log in, in order to view the requested page.")
@login_required
def rejected(request):
    if request.user.is_IC == False:
        messages.info(request, "You don't have access to this page.")
        return redirect('home')
    else:
        if request.method == 'POST':
            data = request.POST
            id = data["submission_id"]
            status_txt = data["status"]

            code = update_status(id, status_txt)
            if code == 1:
                messages.info(request, 'Status updated successfully!')
                
            return redirect('rejected')
        business_unit = BusinessUnit.objects.filter(idea_champion=request.user)
        if business_unit:
            business_unit = business_unit[0]

            submissions = Submission.objects.filter(business_unit=business_unit )
            rejected_submissions = submissions.filter(status="Rejected")

            context = {}
            context['business_unit'] = business_unit
            context['rejected_submissions'] = rejected_submissions

        return render(request, 'mainapp/idea_champion/rejected.html', context)

@login_required_message(message="Please log in, in order to view the requested page.")
@login_required
def add_BU(request):
    if request.user.is_idea_admin == False:
        messages.info(request, "You don't have access to this page.")
        return redirect('home')
    else:
        if request.method == 'POST':
            data = request.POST
            files = request.FILES
            name = data['name']
            idea_champion_txt = data['idea_champion']

            idea_champion = Account.objects.get(email=idea_champion_txt)

            if 'business_unit_img' in files.keys():
                business_unit_img = files['business_unit_img']
                BU = BusinessUnit.objects.create(name=name, idea_champion=idea_champion, image=business_unit_img)
            else:
                BU = BusinessUnit.objects.create(name=name, idea_champion=idea_champion)
            BU.save()

            load_dotenv()
            send_mail(idea_champion.email, f"New BU assigned - {name}", f"Hey {idea_champion.fullname}! You have been assigned a new business unit {name}. Check it out here {os.getenv('WEB_URL')}auth/login/")

            messages.info(request, 'Business Unit added successfully.')
            return redirect('home')
        idea_champions = Account.objects.filter(is_IC=True)
        context = {
            'idea_champions':idea_champions,
        }
        return render(request, 'mainapp/idea_admin/add_BU.html', context)

@login_required_message(message="Please log in, in order to view the requested page.")
@login_required
def invite_IC(request):
    if request.user.is_idea_admin == False:
        messages.info(request, "You don't have access to this page.")
        return redirect('home')
    else:
        if request.method == 'POST':
            data = request.POST
            email = data['email']

            load_dotenv()
            send_mail(email, "You are invited as a Idea Champion.", f"Hey you have been invited as an Idea Champion. Complete the registration process here {os.getenv('WEB_URL')}auth/signup_ic/?email={email}")

            messages.info(request, 'Invite sent successfully.')
            return redirect('home')
        return render(request, 'mainapp/idea_admin/invite_IC.html')