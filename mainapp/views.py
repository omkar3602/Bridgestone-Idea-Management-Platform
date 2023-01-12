from django.shortcuts import render
from .models import BusinessUnit
from userauth.models import Account
from django.http import HttpResponse

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

def new_submission(request):
    return HttpResponse("New submission")