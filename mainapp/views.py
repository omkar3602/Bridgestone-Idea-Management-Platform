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
from django.utils.timezone import localtime

# Create your views here.
def index(request):
    bussiness_units = BusinessUnit.objects.all()
    innovation_champions = Account.objects.filter(is_IC=True)
    
    context = {
        'is_HOMEPAGE':1,
        'selected':'all',
        'bussiness_units':bussiness_units,
        'innovation_champions':innovation_champions,
    }

    if request.user.is_authenticated:
        if request.user.is_IG_admin:
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
            return render(request, 'mainapp/IG_admin/home.html', context)
        elif request.user.is_IC:
            if request.method == 'POST':
                # data = request.POST
                # id = data["submission_id"]
                # status_txt = data["status"]

                # code = update_status(id, status_txt)
                # if code == 1:
                    # messages.info(request, 'Status updated successfully!')

                data = request.POST
                selected = data['selected']

                if selected == "all":
                    my_status = "All"
                elif selected == "review_pending":
                    my_status = "Review Pending"
                elif selected == "accepted":
                    my_status = "Accepted"
                elif selected == "on_hold":
                    my_status = "On Hold"
                elif selected == "rejected":
                    my_status = "Rejected"

                business_unit = BusinessUnit.objects.filter(innovation_champion=request.user)
                if business_unit:
                    business_unit = business_unit[0]
                    submissions = Submission.objects.filter(business_unit=business_unit)
                    if my_status != "All":
                        submissions = submissions.filter(status=my_status)

                    context['selected'] = selected
                    context['business_unit'] = business_unit
                    context['submissions'] = submissions
                return render(request, 'mainapp/innovation_champion/home.html', context)

            business_unit = BusinessUnit.objects.filter(innovation_champion=request.user)
            if business_unit:
                business_unit = business_unit[0]
                submissions = Submission.objects.filter(business_unit=business_unit)

                context['business_unit'] = business_unit
                context['submissions'] = submissions
            return render(request, 'mainapp/innovation_champion/home.html', context)
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

                context['selected'] = selected
                context['submissions'] = submissions
                context['go_to_submissions'] = True
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
            title = data['title']
            identified_problem = data['identified_problem']
            proposed_solution = data['proposed_solution']
            benefit_of_solution = data['benefit_of_solution']
            similar_solutions = data['similar_solutions']

            business_unit_txt = data['business_unit']

            ideator = request.user
            business_unit = BusinessUnit.objects.get(name=business_unit_txt)

            if 'attachment' in files.keys():
                attachment = files['attachment']
                submission = Submission(title=title, identified_problem=identified_problem, proposed_solution=proposed_solution, benefit_of_solution=benefit_of_solution, similar_solutions=similar_solutions, business_unit=business_unit, ideator=ideator, attachment=attachment)
            else:
                submission = Submission(title=title, identified_problem=identified_problem, proposed_solution=proposed_solution, benefit_of_solution=benefit_of_solution, similar_solutions=similar_solutions, business_unit=business_unit, ideator=ideator)
            submission.save()


            innovation_champion_email = business_unit.innovation_champion.email
            ideator_email = ideator.email

            load_dotenv()
            send_mail(innovation_champion_email, f"New Submission received in BU - {business_unit.name}", f"Hey {business_unit.innovation_champion.fullname}! There is a new submission in the business unit {business_unit.name}. Check it out here {os.getenv('WEB_URL')}")
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
def edit_submission(request, id):
    if request.user.is_ideator == False:
        messages.info(request, "You don't have access to this page.")
        return redirect('home')
    else:
        if request.method == 'POST':
            data = request.POST
            files = request.FILES
            title = data['title']
            identified_problem = data['identified_problem']
            proposed_solution = data['proposed_solution']
            benefit_of_solution = data['benefit_of_solution']
            similar_solutions = data['similar_solutions']
            
            submission = Submission.objects.get(id=id)
            submission.title = title
            submission.identified_problem = identified_problem
            submission.proposed_solution = proposed_solution
            submission.benefit_of_solution = benefit_of_solution
            submission.similar_solutions = similar_solutions

            submission.modified_on = localtime()
            business_unit_txt = data['business_unit']

            ideator = request.user
            business_unit = BusinessUnit.objects.get(name=business_unit_txt)

            if 'attachment' in files.keys():
                if submission.attachment:
                    submission.attachment.delete(save=False)
                attachment = files['attachment']
                submission.attachment = attachment
            
            submission.save()

            innovation_champion_email = business_unit.innovation_champion.email
            ideator_email = ideator.email

            load_dotenv()
            send_mail(innovation_champion_email, f"Submission edited in BU - {business_unit.name}", f"Hey {business_unit.innovation_champion.fullname}! There is a edited submission in the business unit {business_unit.name}. Check it out here {os.getenv('WEB_URL')}")
            send_mail(ideator_email, f"Your Submission has been edited.", f"Hey {ideator.fullname}! Your submission in the business unit {business_unit.name} has been edited. Check the status here {os.getenv('WEB_URL')}#YOUR_SUBMISSIONS")

            messages.info(request, 'Idea edited successfully!')
            return redirect('home')

        submission = Submission.objects.get(id=id)
        if request.user != submission.ideator:
            messages.info(request, "You don't have access to this page.")
            return redirect('home')

        context = {
            'submission':submission,
        }
        return render(request, 'mainapp/ideator/edit_submission.html', context)


@login_required_message(message="Please log in, in order to view the requested page.")
@login_required
def delete_submission(request):
    if request.user.is_ideator == False:
        messages.info(request, "You don't have access to this page.")
        return redirect('home')
    else:
        if request.method == 'POST':
            data = request.POST
            id = data['id']
            submission = Submission.objects.get(id=id)

            if request.user != submission.ideator:
                messages.info(request, "You don't have access to this page.")
                return redirect('home')

            if submission.attachment:
                submission.attachment.delete(save=False)

            submission.delete()

            messages.info(request, 'Idea has been deleted.')
            return redirect('home')
        
        return redirect('home')

@login_required_message(message="Please log in, in order to view the requested page.")
@login_required
def individual_submission(request, id):
    if request.user.is_IC == False:
        messages.info(request, "You don't have access to this page.")
        return redirect('home')
    submission = Submission.objects.filter(id=id)
    submission = submission[0]

    context = {
        'submission': submission,
    }
    return render(request, 'mainapp/innovation_champion/individual_idea_page.html', context)

@login_required_message(message="Please log in, in order to view the requested page.")
@login_required
def update_status_view(request):
    if request.user.is_IC == False:
        messages.info(request, "You don't have access to this page.")
        return redirect('home')
    if request.method == 'POST':
        data = request.POST
        id = data["submission_id"]
        status_txt = data["status"]
        remark = data["remark"]

        code = update_status(id, status_txt, remark)
        if code == 1:
            messages.info(request, 'Status updated successfully!')
    return redirect('individual_submission', id=id)

@login_required_message(message="Please log in, in order to view the requested page.")
@login_required
def add_BU(request):
    if request.user.is_IG_admin == False:
        messages.info(request, "You don't have access to this page.")
        return redirect('home')
    else:
        if request.method == 'POST':
            data = request.POST
            files = request.FILES
            name = data['name']
            innovation_champion_txt = data['innovation_champion']

            innovation_champion = Account.objects.get(email=innovation_champion_txt)

            if 'business_unit_img' in files.keys():
                business_unit_img = files['business_unit_img']
                BU = BusinessUnit.objects.create(name=name, innovation_champion=innovation_champion, image=business_unit_img)
            else:
                BU = BusinessUnit.objects.create(name=name, innovation_champion=innovation_champion)
            BU.save()

            load_dotenv()
            send_mail(innovation_champion.email, f"New Business Unit assigned - {name}", f"Hey {innovation_champion.fullname}! You have been assigned a new business unit {name}. Check it out here {os.getenv('WEB_URL')}auth/login/")

            messages.info(request, 'Business Unit added successfully.')
            return redirect('home')
        innovation_champions = Account.objects.filter(is_IC=True)
        context = {
            'innovation_champions':innovation_champions,
        }
        return render(request, 'mainapp/IG_admin/add_BU.html', context)

@login_required_message(message="Please log in, in order to view the requested page.")
@login_required
def invite_IC(request):
    if request.user.is_IG_admin == False:
        messages.info(request, "You don't have access to this page.")
        return redirect('home')
    else:
        if request.method == 'POST':
            data = request.POST
            email = data['email']

            load_dotenv()
            send_mail(email, "You are invited as a Innovation Champion.", f"Hey you have been invited as an Innovation Champion. Complete the registration process here {os.getenv('WEB_URL')}auth/signup_ic/?email={email}")

            messages.info(request, 'Invite sent successfully.')
            return redirect('home')
        return render(request, 'mainapp/IG_admin/invite_IC.html')